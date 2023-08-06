# Copyright 2018-2020 kwantspectrum authors.
#
# This file is part of kwantspectrum.  It is subject to the license terms in
# the file LICENSE.rst found in the top-level directory of this distribution.

from functools import partial
import numpy as np
from numpy.testing import assert_array_almost_equal, assert_array_equal
import pytest
from pytest import raises
import kwant
from .. import kwant_spectrum as ks


def test_cubic_coeffs_raise():
    x = np.array([[1, 2], [3, 4]])
    raises(ValueError, ks._cubic_coeffs, x, np.sin(x), np.cos(x))
    x = np.linspace(-1, 1, dtype=np.complex128)
    raises(ValueError, ks._cubic_coeffs, x, np.sin(x), np.cos(x))
    x = np.array([1])
    raises(ValueError, ks._cubic_coeffs, x, np.sin(x), np.cos(x))
    x = np.linspace(-1, 1)
    raises(ValueError, ks._cubic_coeffs, np.append(x, 2), np.sin(x), np.cos(x))
    raises(ValueError, ks._cubic_coeffs, x, np.sin(x), np.cos(np.append(x, 2)))
    raises(ValueError, ks._cubic_coeffs, x, np.sin(x), 1j * np.cos(x))
    raises(ValueError, ks._cubic_coeffs, x[::-1], np.sin(x), np.cos(x))
    raises(ValueError, ks._cubic_coeffs, x, np.sin(x), np.cos(x), axis=1)
    raises(ValueError, ks._cubic_coeffs, x * np.nan, np.sin(x), np.cos(x))
    raises(ValueError, ks._cubic_coeffs, x, np.sin(x) * np.nan, np.cos(x))
    raises(ValueError, ks._cubic_coeffs, x, np.sin(x), np.cos(x) * np.nan)


def test_interpolation():

    def func(x):
        return np.array([x * (x - 2) * (x + 1), np.exp(1j * x)])

    def df(x):
        return np.array([3 * x * x - 2 * x - 2, 1j * np.exp(1j * x)])

    x = np.linspace(-1, 2, 60)
    xx = np.linspace(-1, 2, 100)
    fint = ks._cubic_interpolation(x, func(x), df(x), axis=1)
    assert_array_almost_equal(fint(xx), func(xx).T)
    assert_array_almost_equal(fint(xx, nu=1), df(xx).T)
    fint = ks._cubic_interpolation(x, func(x).T, df(x).T)
    assert_array_almost_equal(fint(xx), func(xx).T)
    assert_array_almost_equal(fint(xx, nu=1), df(xx).T)

    # test roots:
    def func(x):
        return (x - 0.5) * (x + 0.7) * (x + 0.2)

    def dfunc(x):
        return (x + 0.7) * (x + 0.2) + (x - 0.5) * (x + 0.2) + (x - 0.5) * (x + 0.7)

    x = np.linspace(-1, 1, 50)
    cb = ks._cubic_interpolation(x, func(x), dfunc(x))
    assert_array_almost_equal(cb.roots(), [-0.7, -0.2, 0.5])

    # zeros at interval boundary
    def func(x):
        return (x - 1) * (x + 0.7) * (x + 1)

    def dfunc(x):
        return (x + 0.7) * (x + 1) + (x - 1) * (x + 1) + (x - 1) * (x + 0.7)

    cb = ks._cubic_interpolation(x, func(x), dfunc(x))
    assert_array_almost_equal(cb.roots(), [-1., -0.7, 1.])


def test_symmetric_function_matching():
    # for highly symmetric functions, simple error estimate (eg. midpoint) fail
    def func(x):
        return np.array([[np.cos(x)], [-np.sin(x)]])
    x, *_ = ks._match_functions(func, xmin=-np.pi, xmax=np.pi)
    assert x.size > 3


def test_function_matching():
    def model_func(xx, ordering='magnitude'):
        def f(x):
            return np.array([np.sin(x), -2 * np.cos(2 * x)])

        def df(x):
            return np.array([np.cos(x), 4 * np.sin(2 * x)])

        if ordering == 'magnitude':  # ordering like band structure
            order = np.argsort(f(xx))
        elif ordering == 'random':
            ran = np.random.randint(2, size=1)[0]
            order = np.array([ran, 1 - ran])
        else:  # continous lines
            order = range(len(f(xx)))

        y = f(xx)[order]
        dy = df(xx)[order]

        return np.array([y, dy])

    xx, yy, dyy, *_ = ks._match_functions(model_func, xmin=-5, xmax=5)

    y = [model_func(x, ordering='continous')[0] for x in xx]
    dy = [model_func(x, ordering='continous')[1] for x in xx]

    assert_array_equal(y, yy)
    assert_array_equal(dy, dyy)


def test_gap_detection_tolerance():
    # test that a gap of order `gap` is found by the matching algorithm
    # if the tolerance `tol` is fine enough.
    def gap_function(x, gap, x0):
        # model function for a gap
        dx = x - x0
        dx2 = dx * dx
        gap2 = gap * gap
        xsqrt = np.sqrt(dx2 + gap2)

        def f(x):
            return xsqrt

        def df(x):
            return dx / xsqrt

        return np.array([[f(x), -f(x)], [df(x), -df(x)]])

    def gap_detected(x0, gap, tol):
        func = partial(gap_function, gap=gap, x0=x0)
        x, y, dy, *_ = ks._match_functions(func, -1, 1, tol=tol, min_iter=1)
        yy = func(x)[0].T
        return np.allclose(y, yy)

    for gap in np.power(1 / 10, [i for i in range(3, 8)]):
        for x0 in np.linspace(0.1, 0.9, 9):
            assert not gap_detected(x0, gap, tol=1E-3)
            assert gap_detected(x0, gap, tol=1E-14)


def test_scale_invariance():
    def make_lead(scale=1):
        syst = kwant.Builder(kwant.TranslationalSymmetry((-1, 0)))
        lat = kwant.lattice.square(norbs=1)
        syst[lat(0, 0)] = 1 * scale
        syst[lat(0, 1)] = 8 * scale
        syst[lat(1, 0), lat(0, 0)] = -1 * scale
        syst[lat(1, 1), lat(0, 1)] = 2 * scale
        return syst
    # create two systems at very different energy scales and check that
    # the matching algorithm takes the same number of steps
    # if the bands cross, this test fails, since the estimated crossing
    # position changes slighly due to numerical accuracy of the root finding
    # alorithm, leading to varying number of points in the crossing vicinity
    ba1 = ks.spectrum(make_lead(scale=1E-30).finalized())
    ba2 = ks.spectrum(make_lead(scale=1E30).finalized())
    assert len(ba1.x) == len(ba2.x)


def test_band_analysis_methods():

    # a simple testcase with 3 crossing bands
    def make_lead():
        syst = kwant.Builder(kwant.TranslationalSymmetry((-2, 0)))
        lat = kwant.lattice.square(1, norbs=1)
        syst[lat(0, 0)] = 0
        syst[lat(0, 1)] = 0
        syst[lat(1, 0)] = 0
        syst[lat(1, 0), lat(0, 0)] = 1
        syst[lat(2, 1), lat(0, 1)] = 1
        syst[lat(2, 0), lat(1, 0)] = 0.5
        return syst

    # a simple testcase with 3 non-crossing bands
    def make_simple_lead(W=3):
        lat = kwant.lattice.square(1, norbs=1)
        sym = kwant.TranslationalSymmetry((-1, 0))
        H = kwant.Builder(sym)
        H[(lat(0, y) for y in range(W))] = 0
        H[lat.neighbors()] = -1
        return H

    pi = np.pi

    ba = ks.spectrum(make_lead().finalized())
    # number of bands
    assert ba.nbands == 3
    # momenta, for which band energy = *energy*
    assert len(ba.intersect(f=0, band=0)) == 0
    assert len(ba.intersect(f=0, band=1)) == 0
    assert_array_almost_equal(ba.intersect(f=0, band=2), [-pi / 2, pi / 2])
    # crossings over an extended range
    assert len(ba.intersect(f=0, band=0, kmin=-2 * pi, kmax=3 * pi)) == 0
    assert len(ba.intersect(f=0, band=1, kmin=-2 * pi, kmax=3 * pi)) == 0
    assert_array_almost_equal(ba.intersect(f=0, band=2, kmin=-2 * pi, kmax=3 * pi),
                              np.array([-3, -1, 1, 3, 5]) * pi / 2)
    # zeros of the velocity
    for band in range(ba.nbands):
        velocity_zeros = ba.intersect(f=0, band=band, derivative_order=1)
        assert_array_almost_equal(velocity_zeros, pi * np.array([-1, 0, 1]))
        velocity_zeros = ba.intersect(f=0, band=band, derivative_order=1,
                                      kmin=-3 * pi, kmax=2 * pi)
        assert_array_almost_equal(velocity_zeros,
                                  pi * np.array([-3, -2, -1, 0, 1, 2]))
        # momentum intervals over extended range with band energies: energy <= 0
    intervals = ba.intervals(band=0, upper=0, kmin=-3 * pi, kmax=3 * pi)
    assert_array_almost_equal(intervals, [[-3 * pi, 3 * pi]])
    intervals = ba.intervals(band=1, upper=0, kmin=-3 * pi, kmax=3 * pi)
    assert len(intervals) == 0
    intervals = ba.intervals(band=2, upper=0, kmin=-3 * np.pi, kmax=3 * np.pi)
    assert_array_almost_equal(intervals, [[-3 * pi, -5 / 2 * pi], [-3 / 2 * pi, -1 / 2 * pi],
                                          [1 / 2 * pi, 3 / 2 * pi], [5 / 2 * pi, 3 * pi]])
    # momentum intervals, with band energies: -1.8 <= energy <= 0
    intervals = ba.intervals(band=0, lower=-1.8, upper=0)
    assert_array_almost_equal(intervals, [[-pi, pi]])
    intervals = ba.intervals(band=1, lower=-1.8, upper=0)
    assert len(intervals) == 0
    intervals = ba.intervals(band=2, lower=-1.8, upper=0)
    num_bound = 2.6905658418
    assert_array_almost_equal(intervals,
                              [[-num_bound, -pi / 2], [pi / 2, num_bound]])
    # momentum intervals with positive velocity
    intervals = ba.intervals(band=0, lower=0, derivative_order=1)
    assert_array_almost_equal(intervals, [[0, pi]])
    intervals = ba.intervals(band=1, lower=0, derivative_order=1)
    assert_array_almost_equal(intervals, [[-pi, 0]])
    intervals = ba.intervals(band=2, lower=0, derivative_order=1)
    assert_array_almost_equal(intervals, [[-pi, 0]])
    # momentum intervals, for which band energy <= 0 and velocity > 0
    intervals_e = ba.intervals(band=0, lower=-1.8, upper=0)
    intervals_v = ba.intervals(band=0, lower=0, derivative_order=1)
    intervals = ks.intersect_intervals(intervals_e, intervals_v)
    assert_array_almost_equal(intervals, [[0, pi]])
    intervals_e = ba.intervals(band=1, lower=-1.8, upper=0)
    intervals_v = ba.intervals(band=1, lower=0, derivative_order=1)
    intervals = ks.intersect_intervals(intervals_e, intervals_v)
    assert len(intervals) == 0
    intervals_e = ba.intervals(band=2, lower=-1.8, upper=0)
    intervals_v = ba.intervals(band=2, lower=0, derivative_order=1)
    intervals = ks.intersect_intervals(intervals_e, intervals_v)
    assert_array_almost_equal(intervals, [[-num_bound, -pi / 2]])
    # check energy and velocity interpolant and periodicity
    assert_array_almost_equal(ba.y, ba(ba.x))
    assert_array_almost_equal(ba.y, ba(ba.x + 2 * pi))
    assert_array_almost_equal(ba.y, ba(ba.x - 2 * pi))
    assert_array_almost_equal(ba.dy, ba(ba.x, derivative_order=1))
    assert_array_almost_equal(ba.dy, ba(ba.x + 2 * pi, derivative_order=1))
    assert_array_almost_equal(ba.dy, ba(ba.x - 2 * pi, derivative_order=1))
    # band-mode mapping from momentum
    ba1 = ks.spectrum(make_simple_lead().finalized())
    mode = ba1.momentum_to_scattering_mode
    assert mode(0.1, 2) == mode(-0.1, 2) == 2
    assert mode(1.2, 2) == mode(-1.2, 2) == 1
    assert mode(2.1, 2) == mode(-2.1, 2) == 0
    assert mode(0, 2)
    # band-mode mapping from energy
    mode = ba1.energy_to_scattering_mode
    assert mode(energy=0, band=2, kmin=0, kmax=np.pi) == 2
    assert mode(energy=1, band=2, kmin=0, kmax=np.pi) == 1
    assert mode(energy=3, band=2, kmin=0, kmax=np.pi) == 0
    # check what happens if no mode can be found
    with pytest.warns(UserWarning) as record:
        mode = ba1.energy_to_scattering_mode(0., 0, kmin=0, kmax=1)
    assert len(record) == 1
    assert 'no unique band-mode mapping' in record[0].message.args[0]
    assert mode == -1
    # check that result is similar to reordered kwant result
    bands = kwant.physics.Bands(make_lead().finalized())
    energies = [bands(k)[order] for k, order in zip(ba.x, ba.ordering)]
    assert_array_almost_equal(ba.y, energies)


def test_spectrum_with_flat_band():

    # edgecase with tree bands, where the second band is flat but with tiny noise
    def make_lead_with_flat_band(ll=3):
        lat = kwant.lattice.square(norbs=1)
        lead = kwant.Builder(kwant.TranslationalSymmetry((-1, 1)))
        lead[[lat(0, j) for j in range(ll)]] = 0
        lead[lat.neighbors()] = -1
        return lead

    lead = make_lead_with_flat_band().finalized()
    spectrum = ks.spectrum(lead)

    assert_array_almost_equal([0], spectrum.intersect(f=0, band=0, derivative_order=1))
    assert spectrum.intersect(f=0, band=1, derivative_order=1).size == 0
    assert_array_almost_equal([0], spectrum.intersect(f=0, band=2, derivative_order=1))

    # the spectrum has also no wendepunkt
    assert spectrum.intersect(f=0, band=0, derivative_order=2).size == 0
    assert spectrum.intersect(f=0, band=1, derivative_order=2).size == 0
    assert spectrum.intersect(f=0, band=2, derivative_order=2).size == 0

    # one can lower the tolerance to recover the result with the numerical noise
    assert spectrum.intersect(f=0, band=1, derivative_order=1, ytol=1E-20).size > 0
    assert spectrum.intersect(f=0, band=1, derivative_order=2, ytol=1E-20).size > 0


def test_function_mapping():
    def func(xx):
        # the two functions in f(x) cross at
        # x = [-1, (3 - np.sqrt(13)) / 2, (3 + np.sqrt(13)) / 2]
        def f(x):
            return np.array([x * (x - 2) * (x + 1), x**2 + 2 * x + 1])

        def df(x):
            return np.array([3 * x * x - 2 * x - 2, 2 * x + 2])
        return np.array([f(xx), df(xx)])

    # test function ordering
    # both functions cross at x = (3 + np.sqrt(13)) / 2 = 3.3028
    xl = 2
    xr = 4
    assert_array_equal(func(xr),
                       ks._order_left_to_right(func(xl), func(xr), xl, xr))
    assert_array_equal(func(xr),
                       ks._order_left_to_right(func(xl),
                                               func(xr)[:, [1, 0]], xl, xr))

    xl = -2
    xr = 4
    assert_array_almost_equal([-1],
                              ks._leftmost_crossing(func(xl), func(xr), xl, xr))

    # test function crossing estimate
    xl = 1
    xr = 2
    assert not ks._leftmost_crossing(func(xl), func(xr), xl, xr)

    # test from benoit rossignol where
    # f(-pi) = f(0) = f(pi) = 1 and f'(-pi) = f'(0) = f'(pi) = 0
    # such that the symmetric center point convergence estimate
    # (on the points -pi, 0, pi) fails. if no minimal number of splits
    # is required (which can be simulated by setting min_split = 1) the
    # algorithm will erroneously assume to be converged with only three points.
    def f(x):
        return np.array([[np.cos(2 * x)], [-2 * np.sin(2 * x)]])

    x, y, dy, *_ = ks._match_functions(f, xmin=-np.pi, xmax=np.pi)

    assert len(x) > 3


def test_cost_matrix():
    # take linear functions since cost matrix is calculated in linear approx.
    def func(xx):
        def f(x):
            return np.array([5 * x + 1, -2 * x + 3])
        df = np.array([5, -2])
        return np.array([f(xx), df])

    x0 = 1
    x1 = 3

    # explicit form of the cost matrix
    # m_ij = (\int_x0^x1 (f_i - f_j)^2 dx) / (x1 - x0)
    def fint(x):
        return 49 / 3 * x**3 - 14 * x**2 + 4 * x
    a = (fint(x1) - fint(x0)) / (x1 - x0)

    cost = np.array([[0, a], [a, 0]])
    assert_array_almost_equal(cost,
                              ks._calc_cost_matrix(func(x0), func(x1), x0, x1))


def test_helper_functions():
    assert(ks._intersection((-1, 2), (-0.5, 0.5))
           == ks._intersection((-0.5, 0.5), (-1, 2))
           == (-0.5, 0.5))
    assert(ks._intersection((-1, 2), (1, 3))
           == ks._intersection((1, 3), (-1, 2))
           == (1, 2))
    assert(ks._intersection((-1, 2), (2, 3))
           == ks._intersection((2, 3), (-1, 2))
           == (2, 2))
    assert(ks._intersection((-1, 2), (3, 4)) is None)
    assert(ks._intersection((3, 4), (-1, 2)) is None)

    eps = 1E-14
    # point at pi, -pi ambigous without epsilon
    x = np.linspace(-np.pi + eps, np.pi - eps)
    assert_array_almost_equal(x, ks._periodic(x + 2 * np.pi))
    assert_array_almost_equal(x, ks._periodic(x - 2 * np.pi))

    xeps = np.append(x, x + eps)
    assert_array_equal(x, ks._unique(xeps, tol=2 * eps))

    # TODO: check tolerance
    assert_array_equal(xeps, ks._unique(xeps, tol=eps / 10))
