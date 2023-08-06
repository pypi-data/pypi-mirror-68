# Copyright 2018-2020 kwantspectrum authors.
#
# This file is part of kwantspectrum.  It is subject to the license terms in
# the file LICENSE.rst found in the top-level directory of this distribution.

from functools import partial, wraps
from itertools import tee
import collections.abc
import numpy as np
import scipy.interpolate
from scipy.optimize import linear_sum_assignment
import warnings

from kwant.physics import Bands

__all__ = ['spectrum', 'spectra', 'intersect_intervals', 'BandSketching', '_match_functions']


def _scale_estimate(onsite_hamiltonian, hopping_elements):
    """Estimates maximum/minimum energies of the band structure.

    Returns
    ----------
    emax : float
    emin : float
    """
    norm = np.linalg.norm
    emax = norm(onsite_hamiltonian, ord=2) + 2 * norm(hopping_elements, ord=2)
    emin = norm(onsite_hamiltonian, ord=-2) + 2 * norm(hopping_elements, ord=-2)
    return emax, emin


def _is_type_array(array, generic_type):
    """Return true everywhere where type(array) matches the generic type"""
    array = np.array(array)
    return np.array([_is_type(x, generic_type) for x in array.flatten()])


def _is_type(variable, generic_type):
    """Return true if type(variable) matches the generic type."""
    if generic_type == 'integer':
        return np.issubdtype(type(variable), np.integer)
    if generic_type == 'number':
        return np.issubdtype(type(variable), np.number)
    if generic_type == 'real_number':
        _type = type(variable)
        is_number = np.issubdtype(_type, np.number)
        is_complex = np.issubdtype(_type, np.complexfloating)
        return is_number and not is_complex
    raise NotImplementedError('generic_type= {} not implemented'
                              .format(generic_type))


def _is_zero(x, tol=1e-16):
    """Return true if |x| < tol."""
    return np.abs(x) < tol


def _pairwise(iterable):
    """s -> (s0,s1), (s1,s2), (s2,s3), ..."""
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def _is_inside(x, xmin=None, xmax=None):
    """Check if xmin <= x <= xmax (elementwise if x is an array)."""
    x = np.array(x)
    if xmin is not None and xmax is not None:
        assert xmin <= xmax
        return (xmin <= x) & (x <= xmax)
    if xmin is not None and xmax is None:
        return xmin <= x
    if xmin is None and xmax is not None:
        return x <= xmax
    return np.ones(x.shape, dtype=bool)


def _periodic(k, kmin=-np.pi, kmax=np.pi):
    """Map array elements into :math:`[kmin, kmax]` interval respecting
    periodicity"""
    assert kmin <= kmax, 'bounds swapped'
    period = kmax - kmin
    k = np.where((k >= kmin) & (k <= kmax), k, k % period)
    return np.where(k > kmax, k - period, k)


def _intersection(a, b):
    r"""Finds the intersection :math:`c = a \cap b` of two intervals `a` and `b`.

    Parameters
    ----------
    a, b : array or tuble, float or int
        intervals in form ``(left_bound, right_bound)``

    Returns
    -------
    c : array, float or int
        intersection, has the same data type as `a` and `b`

    Notes
    -----
    Intervals are considered as closed. If both intervals intersect only at one
    point, e.g. a = [0, 1] and b = [1, 2], we return c = [1, 1].
    """
    assert a[0] <= a[1]
    assert b[0] <= b[1]
    if a[0] <= b[0] <= a[1]:
        return b[0], min(b[1], a[1])
    if a[0] <= b[1] <= a[1]:
        return max(b[0], a[0]), b[1]
    if (a[0] <= b[0] and b[1] <= a[1]):
        return b[0], b[1]
    if (b[0] <= a[0] and a[1] <= b[1]):
        return a[0], a[1]
    return None


def _unique(array, tol=1E-16):
    "Remove redundant elements of a float array within a given tolerance."
    unique = []
    for x in array:
        if not np.isclose(unique, x, rtol=tol, atol=tol).any():
            unique.append(x)
    return np.array(unique)


def _is_not_empty(a):
    """Check if a exists."""
    try:
        return a.any()
    except AttributeError:
        if a:
            return True
        return False


def intersect_intervals(interval_a, interval_b, tol=1E-16):
    """Return the intersecting intervals between two lists of intervals."""
    def large_enough(a, b):
        intersect = _intersection(a, b)
        if intersect:
            return not _is_zero(intersect[1] - intersect[0], tol=tol)
        return False
    return [_intersection(a, b) for a in interval_a for b in interval_b
            if large_enough(a, b)]


def _cubic_coeffs(x, y, dy, axis=0):
    """Computes the cubic polynominal coefficients  in `scipy.PPoly` form
    from a function and its first derivative.

    Parameters
    --------
    x : array_like, shape (n,)
        1-d array containing values of the independent variable  (abscissa).
        Values must be real, finite and in strictly increasing order.
    y : array_like
        Array containing values of the function evaluated sampling points `x`.
        It can have arbitrary number of dimensions, but the length along `axis`
        (see below) must match the length of `x`. Values must be finite.
    dy : array_like
        Array containing values of the function derivative evaluated sampling
        points `x`. It can have arbitrary number of dimensions, but the length
        along `axis` (see below) must match the length of `x`.
        Values must be finite. Shape and type must match the `y` values.
    axis : int, optional
        Axis along which `y` is assumed to be varying. Meaning that for
        ``x[i]`` the corresponding values are ``np.take(y, i, axis=axis)``.
        Default is 0.

    Returns
    ----------
    c : ndarray, shape (4, n, ...)
        Coefficients of the cubic polynominal `q(x)` for `n` intervals.
        In the ith interval ``x[i] <= x < x[i+1]``, with ``0 <= i < n``
        the polynominal is of the form:

    `q(x) = c[0, i] (x-x[i])^3 + c[1, i] (x-x[i])^2 + c[2, i] (x-x[i]) + c[3, i]`

    Notes
    ----------
    Algorithm similar to `scipy.interpolate.CubicSpline`
    """
    x = np.asarray_chkfinite(x)
    y = np.asarray_chkfinite(y)
    dy = np.asarray_chkfinite(dy)

    if not 0 <= axis < y.ndim:
        raise ValueError('`axix`={} not between 0 and {}'.format(axis, y.ndim))

    if axis != 0:
        y = np.rollaxis(y, axis)
        dy = np.rollaxis(dy, axis)

    n = x.size
    dx = np.diff(x)

    if x.ndim != 1:
        raise ValueError("`x` must be 1-dimensional")
    if np.issubdtype(x.dtype, np.complexfloating):
        raise ValueError("`x` must contain real values.")
    if x.size < 2:
        raise ValueError('at least two points needed for interpolation')
    if not x.shape[0] == y.shape[0]:
        raise ValueError('input data must have similar size')
    if not y.shape == dy.shape:
        raise ValueError('`y` and `dy` must have similar shape')
    if y.dtype != dy.dtype:
        raise ValueError('type of `y` and `dy` must be identical')
    if not all(dx > 0.0):
        raise ValueError('`x` must be strictly increasing')

    dxr = dx.reshape([dx.shape[0]] + [1] * (y.ndim - 1))
    slope = np.diff(y, axis=0) / dxr

    a = np.zeros((3, n))  # This is a banded matrix representation.
    a[1] = 1
    s = scipy.linalg.solve_banded((1, 1), a, dy, overwrite_ab=True,
                                  check_finite=False)

    # Compute coefficients in PPoly form.
    t = (s[:-1] + s[1:] - 2 * slope) / dxr
    c = np.empty((4, n - 1) + y.shape[1:], dtype=t.dtype)
    c[0] = t / dxr
    c[1] = (slope - s[:-1]) / dxr - t
    c[2] = s[:-1]
    c[3] = y[:-1]

    return c


def _cubic_interpolation(x, y, dy, axis=0, ext=False):
    r"""Return a `scipy.interpolate.PPoly` instance for piecewise cubic
    Hermite interpolation along one direction to a given set function and
    derivative values.

    Parameters
    ----------
    x : array_like, shape (n,)
        1-d array containing values of the independent variable (abscissa).
        Values must be real, finite and in strictly increasing order.
    y : array_like
        Array containing values of the function evaluated sampling points `x`.
        It can have arbitrary number of dimensions, but the length along `axis`
        (see below) must match the length of `x`. Values must be finite.
    dy : array_like
        Array containing values of the function derivative evaluated sampling
        points `x`. It can have arbitrary number of dimensions, but the length
        along `axis` (see below) must match the length of `x`.
        Values must be finite. Shape and type must match the `y` values.
    axis : int, optional
        Axis along which `y` is assumed to be varying. Meaning that for
        ``x[i]`` the corresponding values are ``np.take(y, i, axis=axis)``.
        Default is 0.
    extrapolate : bool, optional
        Whether to extrapolate to ouf-of-bounds points based on first and last
        intervals, or to return NaNs. Default: False.

    Returns
    -------
    ppoly : `scipy.interpolate.PPoly` instance for piecewise cubic
        Hermite interpolation.

    Notes
    -----
    For the piecewise cubic Hermite interpolation of a function :math:`f` we
    take :math:`y_1 \ldots y_n` with :math:`y_i = f(x_i)`  and derivatives
    :math:`dy_1 \ldots dy_n` with :math:`dy_i = f'(x_i)` on sampling points
    :math:`x_1 \ldots x_n`. On each subinterval :math:`[x_i, x_{i+1}]` the two
    function and derivative values determine uniquely the coefficients
    of a cubic interpolation function.
    """
    coeffs = _cubic_coeffs(x, y, dy, axis)
    return scipy.interpolate.PPoly(coeffs, x, extrapolate=ext)


def remove_nan(roots):
    """Remove possible `nan` values from `scipy.interpolate.PPoly.roots`

    Notes
    -----
        From `PPoly.roots` docstring:
        If the piecewise polynomial contains sections that are identically zero,
        the root list will contain the start point of the corresponding interval,
        followed by a nan value.
        This routine will remove the nan as well as the interval start point,
        if there are any.
    """

    root_is_nan = np.isnan(roots)
    if root_is_nan.any():
        for i in range(1, len(root_is_nan), 2):
            if root_is_nan[i]:
                root_is_nan[i - 1] = True
    return roots[~root_is_nan]


def _machine_epsilon_reached(x0, x1):
    """Return `True` if relative difference between `x0` and `x1` is smaller
    than machine epsilon for floats"""
    return np.abs(x0 - x1) <= 10 * np.finfo(np.float).eps


def _leftmost_crossing(fl, fr, xl, xr):
    """Find the leftmost crossing point of an array of functions

    Returns
    ----------
    xmin : list
        smallest value `x` inside interval xl <= x <= xr
        for which two functions cross
        If no crossing occurs, or only one function is given to this routine
        an empty list is returned
    """
    if fl.shape[1] > 1:
        fld = np.diff(fl[0:2])
        frd = np.diff(fr[0:2])
        func = _cubic_interpolation([xl, xr],
                                    [fld[0], frd[0]], [fld[1], frd[1]])
        min_elem = np.array([np.amin(elem) for elem in func.roots()
                             if _is_not_empty(elem)])
        if _is_not_empty(min_elem):
            return [np.amin(min_elem)]
    return []


def _calc_cost_matrix(func0, func1, x0, x1):
    """Calculate a cost matrix used for the linear assignment problem.

    Parameters
    ----------
    func0 : ndarray, shape(2, n)
        vector like function `f` (size n) and its first derivative in form
        `(f, f')` evaluated at position `x0`.
    func1 : ndarray, shape(2, n)
        vector like function `f` (size n) and its first derivative in form
        `(f, f')` evaluated at position `x1`.
    x0 : float
        `x` value (abscissa) at position 0
    x1 : float
        `x` value (abscissa) at position 1

    Returns
    -------
    cost : numpy float array, shape(n, n)
        cost matrix

    Notes
    -----
    Mathematical form of the cost matrix detailed in the notes.
    """
    # linear center approximation
    a0, b0 = func0.reshape(2, -1, 1)
    a1, b1 = func1.reshape(2, 1, -1)

    dx = (x1 - x0) / 2

    a = a0 - a1 + (b0 + b1) * dx
    b = b0 - b1
    pvec = np.array([b * b / 3, 0, a * a])
    return np.polyval(pvec, dx)


def _order_left_to_right(fl, fr, xl, xr):
    """Order the elements of a vector like function on an interval.
    The elements of the function vector on the right boundary are ordered
    according to the element ordering on the left boundary.

    Parameters
    ----------
    fl : ndarray, shape(2, n)
        vector like function `f` (size n) and its first derivative in form
        `(f, f')` evaluated at position `xl`.
    fr : ndarray, shape(2, n)
        vector like function `f` (size n) and its first derivative in form
        `(f, f')` evaluated at position `xr`.
    xl : float
        `x` value (abscissa) at left position
    xr : float
        `x` value (abscissa) at right position

    Returns
    -------
    fr : array like, shape(2, n)
        same as the input `fr` parameter, but the elements of each vector
        `(f, f')` are interchanged in order to match the element ordering
        of the fl input parameter
    ordering : array like, shape(n)
        the ordering vector of the right-hand-side to match the element
        ordering on the left side
    """
    cost = _calc_cost_matrix(fl[0:2], fr[0:2], xl, xr)
    ordering = linear_sum_assignment(cost)[1]
    return fr[:, ordering]


def _cubic_interpolation_error(dx, fl, fc, fr):
    r"""Estimates the error of a cubic interpolant in an interval
    :math:`[x_l, x_r]` employing a 3-point rule:
    :math:`fi = f(x_i),\, dx = x_r - x_l,\, x_c = (x_r + x_l) / 2`

    Parameters
    ----------
    dx : float
        distance between interval boundaries, `dx > 0`
    fl : numpy array, shape (2, ..)
        function `f` and its first derivative in form
        `(f, f')` evaluated at position `xl`
    fc : numpy array, shape (2, ..)
        function `f` and its first derivative in form
        `(f, f')` evaluated at position `xc`
    fr : numpy array, shape (2, ..)
        function `f` and its first derivative in form
        `(f, f')` evaluated at position `xr`

    Returns
    -------
    delta : float
        error estimate for the cubic interpolation function
    """
    fm = (fl[0] + fr[0] - 2 * fc[0]) / 2 + dx / 8 * (fl[1] - fr[1])
    dfm = 3 / 4 * (fr[0] - fl[0]) - dx / 8 * (fl[1] + fr[1] + 4 * fc[1])
    return np.sqrt(39 * fm * fm + dfm * dfm)


def _save_ordering(func):
    """Append an array [0, n-1] on the function result to track reordering"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return np.insert(result, 2, np.arange(result.shape[1]), axis=0)
    return wrapper


def _match_functions(func, xmin=-1, xmax=1, tol=1E-8, min_iter=10,
                     max_iter=100000, interval_converged=None, evaluated=None):
    """Match the elements of a vector valued function, such that
    each vector element describes a continous function.

    Parameters
    ----------
    func : callable
        function `f` to evaluate `(f, f')` for a given abscissa, output
        arraylike with shape (2, n)
    xmin : float or int, optional
        Lower interval boundary to order the function. Defaut = -1.
    xmax : float or int, optional
        Upper interval boundary to order the function. Defaut = 1.
    tol : float, optional
        Numerical tolerance.
    min_iter : int, optional
        Minimal number of iterations of the matching alorithm.
        Defaut = 10
    max_iter : int, optional
        Maximum number of iterations of the matching alorithm. Defaut = 100000
    interval_converged : callable, optional
        Error estimate for the interval.
        Defaut: 3-point estimate for local cubic interpolants
    evaluated : dict, optional
        Dict of precalculated function values

    Returns
    -------
    x : numpy float array, shape (m, )
        abscissa values, where the function has been evaluated
    f : numpy float array, shape (m, n)
        function `f` values
    df : numpy float array, shape (m, n)
        first derivatives `f'` values
    ordering : numpy int array, shape (m, n)
        ordering vector at each evaluation point

    Notes
    -----
    Mathematically, the function that we like to find is the mapping
    :math:`f: R` -> :math:`R^n`, where each vector element itself describes
    a continous function. If the ordering of the elements has been
    interchanged (e.g. we reorder the vector elements always by its magnitude)
    in some countable set of finite regions, we can use this routine
    to retain the continous ordering.
    """

    def order(xl, xr, fr=None):
        # recursive ordering from the left (xl) to the right (xr)

        nonlocal n_calls
        n_calls += 1
        if n_calls > max_iter:
            raise ValueError('maximum iteration limit reached')

        fl = ordered.get(xl)
        if fl is None:
            ordered[xl] = fl = func(xl)

        if fr is None:  # if fr exists, it is has already been matched before
            fr = evaluated.get(xr, func(xr))
            fr = _order_left_to_right(fl, fr, xl, xr)

        # check for numerical tolerance
        dx = xr - xl
        if _machine_epsilon_reached(xl, xr):
            ordered[xr] = fr
        else:
            xc = (xl + xr) / 2
            fc = _order_left_to_right(fl, func(xc), xl, xc)
            if interval_converged(dx, fl, fc, fr):
                ordered[xc] = fc
                ordered[xr] = fr
            else:
                evaluated[xc] = fc
                try:
                    order(xl, xc, fc)
                    order(xc, xr)
                except Exception:
                    return

    # type and input checks
    assert _is_type(xmin, 'real_number')
    assert _is_type(xmax, 'real_number')
    assert _is_type(tol, 'real_number')
    assert _is_type(min_iter, 'integer')
    assert _is_type(max_iter, 'integer')
    assert 0 < min_iter < max_iter
    assert tol > 0
    assert callable(func)

    if interval_converged is None:
        def interval_converged(dx, fl, fc, fr):
            return np.max(_cubic_interpolation_error(dx, fl, fc, fr)) < tol

    if evaluated is None:
        evaluated = {}  # evaluated points, not yet ordered
    ordered = {}  # ordered points
    n_calls = 0

    func = _save_ordering(func)

    try:
        xs = np.linspace(xmin, xmax, min_iter + 1)
        for i in range(min_iter):
            order(xs[i], xs[i + 1])
    except ValueError as err:
        warnings.warn(err)

    x = np.array(sorted(ordered.keys()))
    y = np.array([ordered[xx][0:3] for xx in x])

    # check for consistency before returning
    assert x.size == y.shape[0]
    assert _is_type_array(x, 'number').all()
    assert _is_type_array(y, 'number').all()

    return x, y[:, 0], y[:, 1], y[:, 2].astype(int)


def spectrum(syst, args=(), *, params=None, kmin=-np.pi, kmax=np.pi,
             orderpoint=0, tol=1E-8, match=_match_functions):
    r"""Interpolate the dispersion function and provide methods to
    simplify curve sketching and analyzation the periodic spectrum.

    Parameters
    ----------
    syst : `kwant.system.InfiniteSystem`
        The low level infinite system for which the energies are to be
        calculated.
    args : tuple, defaults to empty
        Positional arguments to pass to the ``hamiltonian`` method.
        Mutually exclusive with 'params'.
    params : dict, optional
        Dictionary of parameter names and their values. Mutually exclusive
        with 'args'.
    kmin : float, optional
        Left-hand site of the momentum interval over which the band structure
        should be analyzed. Defaut = :math:`-\pi`
    kmax : float, optional
        Right-hand site of the momentum interval over which the band structure
        should be analyzed. Defaut = :math:`\pi`
    orderpoint : int or float, optional
        Momentum value where the band ordering is defined. Bands are
        ordered in energy, such that the band with the lowest energy at
        momentum `orderpoint` has index 0. Defaut = 0
    tol : float, optional
        Numerical tolerance of the interpolated function.
    match : callable, optional
        Matching algorithm

    Returns
    -------
    spec : :class:`~kwant_spectrum.BandSketching` instance or a list of these

    Notes
    -----
    The tolerance :math:`tol` is the required precision of the interpolated
    band structure.
    The matching algorithm which orders the bands should work correctly quite
    independently of the tolerance :math:`tol`. However, as the matching
    algorithm uses piecewise cubic interpolations for the error estimate
    internally, the cubic piecewise interpolation should be used for the
    subsequent interpolation of the spectrum for consistency.
    """

    # type and input checks
    assert _is_type(kmin, 'real_number')
    assert _is_type(kmax, 'real_number')
    assert _is_type(orderpoint, 'real_number')
    assert _is_type(tol, 'real_number')
    assert kmin <= kmax, 'bounds swapped'
    assert tol > 0

    # match the bands continously
    def array_function(func):
        """Return energies and first derivative (velocities) as array"""
        @wraps(func)
        def wrapper(*args, **kwargs):
            return np.array(func(*args, **kwargs, derivative_order=1))
        return wrapper

    bands = Bands(syst, args, params=params)
    tol_eff = tol * np.sum(np.abs(_scale_estimate(bands.ham, bands.hop)))
    x, y, dy, ordering = match(array_function(bands), kmin, kmax, tol_eff)

    # order bands according to their energy at momentum `orderpoint`
    band_order = np.argsort(y[np.abs(x - orderpoint).argmin()])
    y = y[:, band_order]
    dy = dy[:, band_order]
    ordering = ordering[:, band_order]

    # provide a function that calculates the open modes for a given energy
    mode_function = partial(syst.modes, args=args, params=params)

    # return a cubic interpolation of the spectrum, provide access to
    # ordering
    band_sketching = BandSketching(x, y, dy, mode_function, tol)
    band_sketching.ordering = ordering
    return band_sketching


def spectra(syst, *args, **kwargs):
    """Interpolates a sequence of dispersion functions and provide methods to
    simplify curve sketching and analyzation the periodic spectra.

    Parameters
    ----------
    syst : :class:`kwant.system.InfiniteSystem` or sequence thereof
        The low level infinite systems.

    Returns
    -------
    specs : list of :class:`~kwant_spectrum.BandSketching`

    Notes
    -----
    The function is similar to :class:`~kwant_spectrum.spectrum` but works as well
    for a sequence of leads. It always returns a list of spectra.
    See :class:`~kwant_spectrum.spectrum` for optional function arguments.
    """
    if not isinstance(syst, collections.abc.Iterable):
        syst = [syst]
    return [spectrum(sys_, *args, **kwargs) for sys_ in syst]


class BandSketching:
    """Interpolate the dispersion function and provide methods to
    simplify curve sketching and analyzation the periodic spectrum.

    Parameters
    ----------
    x : numpy list, shape (n, )
        momentum (k) points
    y : numpy list, shape (n, nbands)
        energy values
    dy : numpy list, shape (n, nbands)
        velocity values
    mode_function : callable
        calculates the open modes for a given energy
    tol : float
        Numerical accuracy of the interpolated function.
    interpolation : object, optional
        Method to perform numerical interpolations.
        Default = cubic Hermite interpolation (piecewise cubic interpolation,
        0. and 1. order of the exact and interpolation function are similar
        on the knots).

    Notes
    -----
    The routine designed for a periodic function that is represented
    as discrete values on a finite gridpoints.
    Finite accuracy of the data and possible unphysical results are taking into
    account by rounding value :math:`tol`.
    """
    def __init__(self, x, y, dy, mode_function, tol=1E-8,
                 interpolation=_cubic_interpolation):

        # type and input checks
        assert x.size == y.shape[0] == dy.shape[0]
        assert y.shape == dy.shape
        assert _is_type_array(x, 'real_number').all()
        assert _is_type_array(y, 'real_number').all()
        assert _is_type_array(dy, 'real_number').all()
        assert callable(mode_function)
        assert _is_type(tol, 'real_number')
        assert tol > 0

        self.x = x
        self.y = y
        self.dy = dy
        self._modes = mode_function
        self.tol = tol
        self.interpolation = interpolation

        self._func = interpolation(x, y, dy)

        self.period = (-np.pi, np.pi)  # default 2 pi periodic spectrum
        self.kmin = x[0]
        self.kmax = x[-1]
        self.nbands = len(y[0])  # the total number of bands

    def __call__(self, k, band=None, derivative_order=0):
        r"""Calculate energies :math:`E` (or optionally higher momentum
        derivatives) for a list of momenta :math:`k`

        Parameters
        ----------
        k : int or float, scalar or array, shape (n, )
            Momentum values where the dispersion is evaluated.
        band : int, optional
            If present, return result only for the
            corresponding band index, requirement: `0 <= band < nbands`.
            Default = None (output for all bands)
        derivative_order : int, optional
            order `m` of the derivative :math:`d^mE / dk^m`. Default = 0.

        Returns
        -------
        energies : numpy array, shape (n, nbands)
            Energies :math:`E_i` (or derivatives) of the bands with
            :math:`n \in \{0, nbands - 1\}`, where
            :math:`nbands` is the number of open modes.

        Notes
        -------
        The bands are ordered continously.
        """
        assert _is_type(derivative_order, 'integer')

        if isinstance(k, (list, tuple, np.ndarray)):
            k = np.array(k)
        if self.period:
            k = _periodic(k, *self.period)
        if __debug__:
            if not _is_type_array(k, 'real_number').all():
                raise TypeError('momenta k must be real numbers')
            if not _is_inside(k, self.kmin, self.kmax).all():
                raise ValueError('momenta k must lie inside sampling interval'
                                 '=[{}, {}]'.format(self.kmin, self.kmax))
        if band is not None:
            assert _is_type(band, 'integer')
            assert 0 <= band < self.nbands, 'band index out of range'
            try:
                return self._func(k, derivative_order)[:, band]
            except IndexError:
                return self._func(k, derivative_order)[band]
        return self._func(k, derivative_order)

    def set_period(self, period):
        """Set periodicity of the spectrum

        Parameters
        ----------
        period : 2-tuple or False
            Perodic interval provided in the form (left_bound, right_bound)
            over which the band structure is assumed as periodic.
            If period is set to false, the dispersion function is evaluated
            as non-periodic fuction and the user has to perform periodic
            mapping herself if needed.
        """
        if __debug__:
            if period:
                if not _is_type_array(period, 'number').all():
                    raise TypeError('elements of period must be real numbers')
                assert period[0] <= period[1], 'bounds swapped'
        self.period = period

    def momentum_to_scattering_mode(self, k, band):
        """Finds the scattering mode index for a band with momentum `k`.

        Parameters
        ----------
        k : float
            momentum value
        band : int
            band index

        Returns
        -------
        mode : int
            kwant scattering mode index.
            The mode index fulfills: `0 <= mode < nbands` where `nbands`
            is the total number of bands of the spectrum.
            If no open mode could be found, `mode = -1` is returned.
        """
        # type checks
        assert _is_type(k, 'real_number')
        assert _is_type(band, 'integer')

        energy = self.__call__(k, band)
        try:  # kwant fails if energy is exactly at the bandgap
            modes = self._modes(energy=energy)[0]
        except ValueError:
            return -1

        momenta = modes.momenta
        velocities = modes.velocities

        # for almost flat bands, small numerical errors (of order 1E-16)
        # in the energy from the interpolation function might fail kwant's
        # mode calculation. (as the velocity of that modes is zero,
        # they do not contribute to a manybody sum anyhow).
        try:
            return np.abs(momenta[velocities > 0] - k).argmin()
        except ValueError:
            return -1

    def energy_to_scattering_mode(self, energy, band, kmin, kmax):
        """Finds the scattering mode index for a band giving its energy.

        Parameters
        ----------
        energy : float
        band : int
            band index
        kmin, kmax: float
            momentum interval ``[kmin, kmax]`` including the searched momentum,
            where the velocity does not change sign

        Returns
        -------
        mode : int
            kwant scattering mode index
            The mode index fulfills: `0 <= mode < nbands` where `nbands`
            is the total number of bands of the spectrum.
            If no open mode could be found, `mode = -1` is returned.
        Notes
        -----
        An exception is raised if the momentum interval [kmin, kmax] is badly
        chose, such that either no mode / multiple modes are found, and
        therefore no unique (energy, band) -> mode mapping is possible,
        a warning is printed.
        """
        # type checks
        assert _is_type(energy, 'real_number')
        assert _is_type(band, 'integer')
        assert _is_type(kmin, 'real_number')
        assert _is_type(kmax, 'real_number')

        k = self.intersect(energy, band, kmin=kmin, kmax=kmax)
        if len(k) != 1:  # test for existance and uniqueness
            msg = ('no unique band-mode mapping: energy={energy}, band={band}, '
                   'interval=[{kmin}, {kmax}], k={k}.'
                   .format(energy=energy, band=band, kmin=kmin, kmax=kmax, k=k))
            warnings.warn(msg)
            return -1
        return self.momentum_to_scattering_mode(k[0], band)

    def intersect(self, f, band, derivative_order=0,
                  kmin=None, kmax=None, tol=None, ytol=None):
        r"""Returns all momentum (k) points, that solves the equation:
        :math:`\partial_k^{n} E(k) = f(k),\, k_{min} \leq k \leq k_{max}`.

        Parameters
        ----------
        f : scalar numerical value or callable
            Equation to solve :math:`\partial_k^{n} E(k) = f`.
            If `f` is callable, solve equation:
            :math:`\partial_k^{n} E(k) = f(k)`.
        band : int
            band index, requirement: `0 <= band < nbands`.
        derivative_order : int, optional
            Derivative order (n) of the band dispersion. Default is zero.
        kmin : scalar numeric value, optional
            Lowest `k` point value. Default is `kmin` from initialization.
        kmax : scalar numeric value, optional
            Largest `k` point value. Default is `kmax` from initialization.
        tol : float, optional
            Numerical tolerance, `k` points closer tol are merged to the same
            point. Default is the `tol` from initialization.
        ytol : float, optional
            Numerical tolerance to remove noise if the
            spectrum :math:`\partial_k^{n} E(k)` is almost flat.
            Values for the spectrum are set to thier mean value
            (averaged over all momentum points where the band is sampled), if
            they flucutate more than `ytol`.
            Default is the `tol` from initialization.

        Returns
        -------
        k : numpy list.
            List of momentum (k) points, that solves the above equation.

        Notes
        -----
        `kmin` and `kmin` can be larger than the first Brillouin zone. In that
        case we return also the periodic images.
        """

        if kmin is None:
            kmin = self.kmin
        if kmax is None:
            kmax = self.kmax
        if tol is None:
            tol = self.tol
        if ytol is None:
            ytol = self.tol

        # type and input checks
        assert _is_type(band, 'integer')
        assert _is_type(derivative_order, 'integer')
        assert _is_type(kmin, 'real_number')
        assert _is_type(kmax, 'real_number')
        assert _is_type(tol, 'real_number')
        assert _is_type(ytol, 'real_number')
        assert 0 <= band < self.nbands, 'band index out of range'
        assert kmin <= kmax, 'bounds swapped'
        assert tol > 0
        assert ytol > 0
        # check if the interval [kmin, kmax] is entirely inside the samling
        # interval [self.kmin, self.kmax]. if not, apply periodic mapping.
        # we have to check however if the required period is smaller or
        # equal the sampling interval
        if not _is_inside([kmin, kmax], self.kmin, self.kmax).all():
            if not _is_inside(self.period, self.kmin, self.kmax).all():
                raise ValueError('Sample interval too small')

        if callable(f):
            f = f(self.x)

        if derivative_order == 0:  # use tabulated values, faster
            y = self.y[:, band]
            dy = self.dy[:, band]
        else:
            y = self._func(self.x, derivative_order)[:, band]
            dy = self._func(self.x, derivative_order + 1)[:, band]

        # filter numerical noise if curve is flat
        y_mean = np.mean(y)
        if _is_zero(y_mean, ytol):
            y_mean = 0
        y[np.abs(y - y_mean) < ytol] = y_mean
        dy[np.abs(dy) < ytol] = 0

        roots = self.interpolation(self.x, y - f, dy).roots()
        roots = remove_nan(roots)

        if self.period:
            roots = _periodic(roots, *self.period)

        try:
            period_len = self.period[1] - self.period[0]
            npe = int((kmax - kmin) // period_len)  # number of periods
            images = period_len * np.arange(-npe + 1, npe).reshape(2 * npe - 1, -1)
            roots = _unique(np.sort(np.ravel(roots + images)), tol)
        except:  # no periodic image, npe = 0
            roots = _unique(np.sort(roots), tol)

        return roots[_is_inside(roots, kmin, kmax)]

    def intervals(self, band, derivative_order=0, lower=None, upper=None,
                  kmin=None, kmax=None, tol=None):
        r"""returns a list of momentum (`k`) intervals that solves the equation
        :math:`\text{lower} \leq  \partial^m_k E_n(k)  \leq \text{upper}`

        Parameters
        ----------
        band : int
            band index `n`, requirement: `0 <= n < nbands`.
        derivative_order : int, optional
            Derivative order `m` of the band dispersion. Default is zero.
        lower : int or float, optional
            Select intervals such that
            :math:`\partial_k^{m} E_n(k) \geq \text{lower}`
        upper : int or float, optional
            Select intervals such that
            :math:`\partial_k^{m} E_n(k) \leq \text{upper}`
        kmin : scalar numeric value, optional
            Lowest `k` point value. Default is `kmin` from initialization.
        kmax : scalar numeric value, optional
            Largest `k` point value. Default is `kmax` from initialization.
        tol : float, optional
            Tolerance of the interval selection, such that intervals smaller
            `tol` are neglected and two intervals closer `tol` are merged.

        Returns
        -------
        intervals : list.
            Ordered list of momentum intervals :math:`[k_i, k_{i+1}]`.
            Each interval is given in form of a tuple.
        """

        def f(k):
            return self.__call__(np.mean(k), band, derivative_order)

        if kmin is None:
            kmin = self.kmin
        if kmax is None:
            kmax = self.kmax
        if tol is None:
            tol = self.tol

        # type and input checks
        assert _is_type(band, 'integer')
        assert _is_type(derivative_order, 'integer')
        assert _is_type(kmin, 'real_number')
        assert _is_type(kmax, 'real_number')
        assert _is_type(tol, 'real_number')
        assert 0 <= band < self.nbands, 'band index out of range'
        assert kmin <= kmax, 'bounds swapped'
        assert tol > 0

        crossings = [kmin, kmax]
        if lower is not None:
            crossings = np.append(crossings, self.intersect(lower, band,
                                                            derivative_order,
                                                            kmin, kmax, tol))

        if upper is not None:
            crossings = np.append(crossings, self.intersect(upper, band,
                                                            derivative_order,
                                                            kmin, kmax, tol))

        crossings = _unique(np.sort(crossings), tol)

        return [x for x in _pairwise(crossings)
                if (not _is_zero(x[1] - x[0], tol)
                    and _is_inside(f(x), lower, upper))]
