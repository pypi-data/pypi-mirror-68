###############################################################################
# SpaceRocks, version 0.5.1
#
# Author: Kevin Napier kjnapier@umich.edu
################################################################################

import sys
import random

import healpy as hp

import numpy as np

from scipy.optimize import newton

from skyfield.api import Topos, Loader

from astropy import units as u
from astropy.table import Table
from astropy.coordinates import Angle
from astropy.constants import c

import matplotlib.pyplot as plt
from numba import jit
import pandas as pd

from .linalg3d import dot, norm, cross, euler_rotation

# to do: implement obscode
# to do: implement plotting distributions
# to do: complete polite kwarg rejection
# to do: test everything. write unit tests.

# Load in planets for ephemeride calculation.
load = Loader('./Skyfield-Data', expire=False, verbose=False)
ts = load.timescale()
planets = load('de423.bsp')
sun = planets['sun']
earth = planets['earth']

# standard gravitational parameter, GM, M is the mass of sun + all planets
mu_bary = (4 * np.pi**2) * 1.0013418393275118 * u.radian**2 * u.au**3 / u.year**2
mu_helio = (4 * np.pi**2) * u.radian**2 * u.au**3 / u.year**2

# obliquity of the Earth
epsilon = Angle(23.43929111, u.degree).radian

# speed of light
c = c.to(u.au / u.year)

# G parameter for magnitude estimation
G = 0.15

class SpaceRock:

    def __init__(self, input_coordinates='keplerian', input_frame='barycentric',
                 input_angles='degrees', precise=False, NSIDE=None, obscode=None,
                 uncertainties=None, *args, **kwargs):

        self.precise = precise

        if (self.precise is not True) and (self.precise is not False):
            print('The parameter precise must be set to either True or False.')
            sys.exit()

        # Only used for the topocentric calculation.
        if self.precise == True:
            if obscode is not None:
                self.obscode = obscode
                earth += Topos('30.169 S', '70.804 W', elevation_m=2200) # topocentric calculation

        # Case-insensitive keyword arguments.
        kwargs = {key.lower(): data for key, data in kwargs.items()}
        keywords = ['a', 'e', 'inc', 'node', 'arg', 'M',
                    'x', 'y', 'z', 'vx', 'vy', 'vz',
                    'tau', 'epoch', 'h', 'name']

        #if args is not None:
    #        raise ValueError('SpaceRock doesn\'t take any non-keyword arguments.')

        if not all(key in keywords for key in [*kwargs]):
            print('Keywords are limited to a, e, inc, node, \
                   arg, M, x, y, z, vx, vy, vz, tau, epoch,\
                   H, name')
            sys.exit()

        input_coordinates = input_coordinates.lower()
        input_frame = input_frame.lower()
        input_angles = input_angles.lower()

        # scalar input -> arrays
        for idx, key in enumerate([*kwargs]):
            if np.isscalar(kwargs.get(key)):
                kwargs[key] = np.array([kwargs.get(key)])

        if NSIDE is not None:
            if np.isscalar(NSIDE):
                NSIDE = np.array([NSIDE])
            self.NSIDE = NSIDE
        else:
            self.NSIDE = None

        if input_angles == 'degrees':
            angle_unit = u.degree
        elif input_angles == 'radians':
            angle_unit = u.radian
        else:
            raise ValueError('The input_angles argument must be a string \
                              that reads either degrees or radians.')

        if input_coordinates == 'keplerian':

            self.frame = input_frame
            self.a = kwargs.get('a') * u.au
            self.e = kwargs.get('e') * u.dimensionless_unscaled
            self.inc = Angle(kwargs.get('inc'), angle_unit).to(u.rad)
            self.node = Angle(kwargs.get('node'), angle_unit).to(u.rad)
            self.arg = Angle(kwargs.get('arg'), angle_unit).to(u.rad)
            self.H = kwargs.get('h') #* u.dimensionless_unscaled
            self.tau = kwargs.get('tau') * u.day # obs_date

            if kwargs.get('name') is not None:
                self.name = kwargs.get('name')
            else:
                # produces random, non-repeting integers between 0 and 1e10 - 1
                self.name = ['{:010}'.format(value) for value in random.sample(range(int(1e10)), len(self.a))]


            if input_frame == 'barycentric':

                if (kwargs.get('epoch') is None) and (kwargs.get('M') is not None):
                    self.M = Angle(kwargs.get('M'), angle_unit) * u.rad
                    self.epoch = self.tau - self.M / np.sqrt(mu_bary / self.a**3)

                elif (kwargs.get('M') is None) and (kwargs.get('epoch') is not None):
                    self.epoch = kwargs.get('epoch') * u.day # time at perihelion
                    self.M = np.sqrt(mu_bary / self.a**3) * (self.tau - self.epoch)

                self.x, self.y, self.z, self.vx, self.vy, self.vz = self.kep_to_xyz(mu_bary)
                self.r = norm([self.x, self.y, self.z])
                self.ra, self.dec, self.delta, self.ltt, self.phase_angle, self.elong = self.xyz_to_equa()

            # If the input frame is heliocentric, convert to bary to calculate
            # equatorial coordinates. Then go back to heliocentric.
            elif input_frame == 'heliocentric':

                if (kwargs.get('epoch') is None) and (kwargs.get('M') is not None):
                    self.M = Angle(kwargs.get('M'), angle_unit) * u.rad
                    self.epoch = self.tau - self.M / np.sqrt(mu_helio / self.a**3)

                elif (kwargs.get('M') is None) and (kwargs.get('epoch') is not None):
                    self.epoch = kwargs.get('epoch') * u.day # time at perihelion
                    self.M = np.sqrt(mu_helio / self.a**3) * (self.tau - self.epoch)

                self.x, self.y, self.z, self.vx, self.vy, self.vz = self.kep_to_xyz(mu_helio)

                # convert to barycentric to calculate equatorial coordinates
                self.to_bary()
                self.frame = 'barycentric'

                self.r = norm([self.x, self.y, self.z])
                self.ra, self.dec, self.delta, self.ltt, self.phase_angle, self.elong = self.xyz_to_equa()
                self.mag = self.estimate_mag()

                # convert back to heliocentric to match input frame
                self.to_helio()
                self.frame = 'heliocentric'


        elif input_coordinates == 'cartesian':

            self.frame = input_frame

            self.x = kwargs.get('x') * u.au
            self.y = kwargs.get('y') * u.au
            self.z = kwargs.get('z') * u.au
            self.vx = kwargs.get('vx') * (u.au / u.year)
            self.vy = kwargs.get('vy') * (u.au / u.year)
            self.vz = kwargs.get('vz') * (u.au / u.year)


            if kwargs.get('name') is None:
                self.name = ['rock{}'.format(idx) for idx in range(len(self.x))]
            else:
                self.name = kwargs.get('name')

            if input_frame == 'barycentric':
                self.r = norm([self.x, self.y, self.z])
                self.a, self.e, self.inc, self.arg, self.node, self.M = self.xyz_to_kep(mu_bary)
                self.ra, self.dec, self.delta, self.ltt, self.phase_angle, self.elong = self.xyz_to_equa()

            # If the input frame is heliocentric, convert to bary to calculate
            # equatorial coordinates. Then go back to heliocentric.
            elif input_frame == 'heliocentric':

                self.a, self.e, self.inc, self.arg, self.node, self.M = self.xyz_to_kep(mu_helio)

                # convert to barycentric to calculate equatorial coordinates
                self.to_bary()
                self.frame = 'barycentric'

                self.r = norm([self.x, self.y, self.z])
                self.ra, self.dec, self.delta, self.ltt, self.phase_angle, self.elong = self.xyz_to_equa()

                # convert back to heliocentric to match input frame
                self.to_helio()
                self.frame = 'heliocentric'


        self.varpi = (self.arg + self.node).wrap_at(2 * np.pi * u.rad)
        self.mag = self.estimate_mag()
        if NSIDE is not None:
            for value in self.NSIDE:
                setattr(SpaceRock,
                        'HPIX_{}'.format(value),
                        self.radec_to_hpix(value))


    def cal_E(self, e, M):
        '''
        This method employs Newton's method to solve Kepler's Equation.
        '''
        f = lambda calc_E, M, e: calc_E - e * np.sin(calc_E) - M
        E0 = M
        calc_E = newton(f, E0, args=(M, e))
        return calc_E

    def xyz_to_equa(self):
        '''
        Transform from barycentric Cartesian coordinates to equatorial
        coordinates. If you need very precise values, the method will use
        a topocentric correction to the Earth's position.
        See https://en.wikipedia.org/wiki/Horizontal_coordinate_system.
        This results in a significant slowdown to the code.
        '''
        if self.precise == True:

            t = ts.tt(jd=self.epoch.value)
            x_earth, y_earth, z_earth = earth.at(t).position.au * u.au # earth ICRS position
            earth_dis = norm([x_earth, y_earth, z_earth])
            x0, y0, z0 = self.x, self.y, self.z
            for idx in range(3):
                # transfer ecliptic to ICRS and shift to Geocentric (topocentric)
                x = x0 - x_earth
                y = y0 * np.cos(epsilon) - z0 * np.sin(epsilon) - y_earth
                z = y0 * np.sin(epsilon) + z0 * np.cos(epsilon) - z_earth
                delta = norm([x, y, z])
                ltt = delta / c
                M = self.M - ltt * (mu_bary / self.a**3)**0.5
                if idx < max(range(3)):
                    x0, y0, z0, _, _, _ = self.kep_to_xyz(mu_bary)
            # Cartesian to spherical coordinate
            dec = Angle(np.arcsin(z / norm([x, y, z])), u.rad)
            ra = Angle(np.arctan2(y, x), u.rad).wrap_at(2 * np.pi * u.rad)
            phase_angle = Angle(np.arccos(-(earth_dis**2 - self.r**2 - delta**2)/(2 * self.r* delta)), u.rad)
            elong = Angle(np.arccos(-(self.r**2 - delta**2 - earth_dis**2)/(2 * delta * earth_dis)), u.rad)

        else:
            t = ts.tt(jd=self.epoch.value)
            x_earth, y_earth, z_earth = earth.at(t).position.au * u.au # earth ICRS position
            earth_dis = norm([x_earth, y_earth, z_earth])
            # transfer ecliptic to ICRS and shift to Geocentric (topocentric)
            dx = self.x - x_earth
            dy = self.y * np.cos(epsilon) - self.z * np.sin(epsilon) - y_earth
            dz = self.y * np.sin(epsilon) + self.z * np.cos(epsilon) - z_earth
            delta = norm([dx, dy, dz])
            ltt = delta / c

            # Cartesian to spherical coordinate
            dec = Angle(np.arcsin(dz/delta), u.rad)
            ra = Angle(np.arctan2(dy, dx), u.rad).wrap_at(2 * np.pi * u.rad)

            phase_angle = Angle(np.arccos(-(earth_dis**2 - self.r**2 - delta**2)/(2 * self.r* delta)), u.rad)
            elong = Angle(np.arccos(-(self.r**2 - delta**2 - earth_dis**2)/(2 * delta * earth_dis)), u.rad)

        return ra, dec, delta, ltt, phase_angle, elong

    @jit
    def cal_E_fast(self):
        calc_E = self.M
        for kk in range(100):
            calc_E = self.M + self.e * np.sin(calc_E) * u.rad
        return calc_E

    def radec_to_hpix(self, NSIDE):
        '''
        Convert (ra, dec) into healpix
        '''
        return hp.pixelfunc.ang2pix(NSIDE, np.pi/2 - self.dec.radian, self.ra.radian, nest=True)

    def estimate_mag(self):
        '''
        Estimate the apparent magnitude of a TNO
        '''
        q = (self.r**2 + self.delta**2 - 1 * u.au**2)/(2 * self.r * self.delta)

        ## pyephem
        beta = np.zeros(len(q))
        beta[np.where(q <= 1)[0]] = np.pi * u.rad
        beta[np.where(q >= 1)[0]] = 0 * u.rad

        Psi_1 = np.exp(-3.33 * np.tan(beta/2)**0.63)
        Psi_2 = np.exp(-1.87 * np.tan(beta/2)**1.22)
        mag = self.H + 5 * np.log10(self.r * self.delta / u.au**2)

        not_zero = np.where((Psi_1 != 0) | (Psi_2 != 0))[0]
        mag[not_zero] -= 2.5 * np.log10((1 - G) * Psi_1[not_zero] + G * Psi_2[not_zero])
        return mag

    def kep_to_xyz(self, mu):
        '''
        Transform from Keplerian to cartesian coordinates. There is no analytic
        solution to solve Kepler's Equation M = E - eSin[e] for the eccentric
        anomaly, E. If you need very precise coordinates, the method uses Newton's
        root-finding method from scipy.optimize. This is very precise, but it is
        not vectorizable or compilable, so it is rather slow
        (> factor of 5 slowdown). Otherwise, the .ethod uses a fixed-point
        iteration method. See https://en.wikipedia.org/wiki/Kepler%27s_equation
        '''
        # compute eccentric anomaly E
        if self.precise == True:
            E = np.array(list(map(self.cal_E, self.e.value, self.M.value))) * u.rad
        else:
            E = self.cal_E_fast()

        # compute true anomaly v
        ν = 2 * np.arctan2((1 + self.e)**0.5*np.sin(E/2.), (1 - self.e)**0.5*np.cos(E/2.))

        # compute the distance to the central body r
        r = self.a * (1 - self.e*np.cos(E))

        # obtain the position o and velocity ov vector
        o = [r * np.cos(ν), r * np.sin(ν), np.zeros(len(ν))]
        ov = [(mu * self.a)**0.5 / r * (-np.sin(E)),
              (mu * self.a)**0.5 / r * ((1-self.e**2)**0.5 * np.cos(E)),
              np.zeros(len(ν))]

        # Rotate o and ov to the inertial frame
        x, y, z = euler_rotation(self.arg, self.inc, self.node, o) * u.au
        vx, vy, vz = euler_rotation(self.arg, self.inc, self.node, ov) * u.au / u.year

        return x, y, z, vx, vy, vz

    def xyz_to_kep(self, mu):
        '''
        Transform from Cartesian to Keplerian coordinates. The units in this method
        are a bit hacky due to unexpected behavior and known issues with astropy
        units. But it returns the correct values with the correct units.
        '''
        ## there are a lot of hacky units in here because astropy doesn't behave as expected.
        # compute the barycentric distance r
        r = norm([self.x, self.y, self.z])
        rrdot = dot([self.x, self.y, self.z], [self.vx, self.vy, self.vz])

        # compute the specific angular momentum h
        hx, hy, hz = cross([self.x, self.y, self.z], [self.vx, self.vy, self.vz])
        h = norm([hx, hy, hz])

        # compute eccentricity vector
        ### hacky units
        ex, ey, ez = u.au**3 / u.yr**2 * np.array(cross([self.vx, self.vy, self.vz], \
                     [hx, hy, hz])) *u.rad**2 / mu  - [self.x, self.y, self.z]*u.au/r
        e = norm([ex, ey, ez])

        # compute vector n
        ### hacky units
        nx, ny, nz = -hy.value, hx.value, np.zeros(len(hz))
        n = norm([nx, ny, nz])

        # compute true anomaly ν, the angle between e and r
        ν = np.arccos(dot([ex, ey, ez], [self.x, self.y, self.z]) / (e*r))
        ν[rrdot < 0] = 2 * np.pi * u.rad - ν[rrdot < 0]

        # compute inclination
        inc = np.arccos(hz/h)

        # compute eccentric anomaly E
        E = 2 * np.arctan2(np.sqrt(1-e) * np.sin(ν/2), np.sqrt(1+e) * np.cos(ν/2))

        # compute ascending node
        node = np.arccos(nx/n) * u.rad
        node[ny < 0] = 2 * np.pi * u.rad - node[ny < 0]

        # compute argument of periapsis, the angle between e and n
        arg = np.arccos(dot([nx, ny, nz], [ex, ey, ez]) / (n*e))
        arg[ez < 0] = 2 * np.pi * u.rad - arg[ez < 0]

        # compute mean anomaly
        M = E - e * np.sin(E) * u.rad
        M[M < 0] += 2 * np.pi * u.rad

        # compute a
        a = 1 / (2 / r - norm([self.vx, self.vy, self.vz])**2 / mu * u.rad**2)

        return a, e, inc, arg, node, M

    def to_bary(self):
        '''
        Method to convert heliocentric coordinates to barycentric coordinates.
        '''
        if self.frame == 'heliocentric':
            t = ts.tt(jd=self.epoch.value) #37 leap seconds
            x_sun, y_sun, z_sun = sun.at(t).position.au * u.au
            vx_sun, vy_sun, vz_sun = (sun.at(t).velocity.au_per_d * u.au / u.day).to(u.au / u.year)
            # calculate the barycentric xyz postion
            self.x = self.x + x_sun
            self.y = self.y + y_sun * np.cos(epsilon) - z_sun * np.sin(-epsilon)
            self.z = self.z + y_sun * np.sin(-epsilon) + z_sun * np.cos(epsilon)
            self.vx = self.vx + vx_sun
            self.vy = self.vy + vy_sun * np.cos(epsilon) - vz_sun * np.sin(-epsilon)
            self.vz = self.vz + vy_sun * np.sin(-epsilon) + vz_sun * np.cos(epsilon)

            # calculate barycentric keplerian elements
            self.a, self.e, self.i, self.arg, self.node, self.M = self.xyz_to_kep(mu_bary)

            self.frame = 'barycentric'

        return self

    def to_helio(self):
        '''
        Method to convert barycentric coordinates to heliocentric coordinates.
        '''
        if self.frame == 'barycentric':
            t = ts.tt(jd=self.epoch.value)
            x_sun, y_sun, z_sun = sun.at(t).position.au * u.au
            vx_sun, vy_sun, vz_sun = (sun.at(t).velocity.au_per_d * u.au / u.day).to(u.au / u.year)
            # calculate the heliocentric xyz postion
            self.x = self.x - x_sun
            self.y = self.y - y_sun * np.cos(epsilon) + z_sun * np.sin(-epsilon)
            self.z = self.z - y_sun * np.sin(-epsilon) - z_sun * np.cos(epsilon)
            self.vx = self.vx - vx_sun
            self.vy = self.vy - vy_sun * np.cos(epsilon) + vz_sun * np.sin(-epsilon)
            self.vz = self.vz - vy_sun * np.sin(-epsilon) - vz_sun * np.cos(epsilon)
            self.r = norm([self.x, self.y, self.z])
            # calculate heliocentric keplerian elements
            self.a, self.e, self.i, self.arg, self.node, self.M = self.xyz_to_kep(mu_helio)

            self.frame = 'heliocentric'

        return self

    def get_dict(self):
        '''
        Create a dictionary of the object attributes. This method is used
        by the pandas_df and astropy_table methods.
        '''
        data = {'name':self.name,
                'a':self.a,
                'e':self.e,
                'inc':self.inc,
                'arg':self.arg,
                'node':self.node,
                'varpi':self.varpi,
                'epoch':self.epoch,
                'M':self.M,
                'tau':self.tau,
                'x':self.x,
                'y':self.y,
                'z':self.z,
                'vx':self.vx,
                'vy':self.vy,
                'vz':self.vz,
                'ra':self.ra,
                'dec':self.dec,
                'delta':self.delta,
                'ltt':self.ltt,
                'phase_angle':self.phase_angle,
                'elong':self.elong,
                'mag':self.mag,
                'H':self.H,
                'r':self.r}

        if self.NSIDE is not None:
            for value in self.NSIDE:
                data['HPIX_{}'.format(value)] = getattr(SpaceRock, 'HPIX_{}'.format(value))

        return data

    def pandas_df(self):
        '''
        Write the rocks to a pandas dataframe. Pandas can't hamdle astropy
        units (yet), so if you want to keep units intact you'll have to use
        an Astropy Table.
        '''
        return pd.DataFrame(self.get_dict())

    def astropy_table(self):
        '''
        Write the rocks to an astropy table. This can handle units, though
        it is generally less elegant than pandas.
        '''
        return Table(self.get_dict())

    def write_to_csv(self, path):
        '''
        Write the data to a csv.
        '''
        df = self.pandas_df()
        df.to_csv(path)
        return 'Data written to {}.csv.'.format(path)

    def plot_radec(self, color='black', alpha=0.5):
        '''
        Plot the right ascension and declination of each object on a Mollweide
        projection. (See https://en.wikipedia.org/wiki/Mollweide_projection)
        '''
        fig = plt.figure(figsize=(12, 8))
        ax = fig.add_subplot(111, projection="mollweide")

        xdata = self.ra
        xdata[xdata.value > np.pi] -= 2*np.pi * u.rad

        plt.scatter(xdata, self.dec, color=color, alpha=alpha)
        return

    def predict(self, obsdate):
        '''
        Predict the sky position of a rock on the specified date. You can
        input either one date (JD) that will apply to each object, or an
        array of the length of the number of objects.
        '''
        if self.frame == 'barycentric':
            mu = mu_bary
        elif self.frame == 'heliocentric':
            mu = mu_helio
        else:
            print('The frame must be either heliocentric or \
                   barycentric. Did you change it manually?')
            sys.exit()

        self.tau = obsdate * u.day


        self.M += (mu/self.a**3)**0.5 * (self.tau - self.epoch)
        self.x, self.y, self.z, self.vx, self.vy, self.vz = self.kep_to_xyz(mu)

        if self.frame == 'barycentric':
            self.r = norm([self.x, self.y, self.z])
            self.ra, self.dec, self.delta, self.ltt, self.phase_angle, self.elong = self.xyz_to_equa()

        # If the input frame is heliocentric, convert to bary to calculate
        # equatorial coordinates. Then go back to heliocentric.
        elif self.frame == 'heliocentric':

            # convert to barycentric to calculate equatorial coordinates
            self.to_bary()
            self.frame = 'barycentric'

            self.r = norm([self.x, self.y, self.z])
            self.ra, self.dec, self.delta, self.ltt, self.phase_angle, self.elong = self.xyz_to_equa()

            # convert back to heliocentric to match input frame
            self.to_helio()
            self.frame = 'heliocentric'

        self.mag = self.estimate_mag()

        if self.NSIDE is not None:
            for value in self.NSIDE:
                setattr(SpaceRock, 'HPIX_{}'.format(value), self.radec_to_hpix(value))

        return self

    def plot_distributions(self):
        return
