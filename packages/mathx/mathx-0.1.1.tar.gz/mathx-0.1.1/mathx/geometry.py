import math
import numpy as np
from scipy.ndimage.interpolation import map_coordinates

import mathx
from mathx import usv


def subtract_tangent(x,y,x_0,axis=None):
    if axis==None:
        axis=mathx.last_axis(x)
    y_0=mathx.interp_at(x, y, x_0, [0, 1])
    return y-y_0[0]-(x-x_0)*y_0[1]


def line_two_points(x1, y1, x2, y2, x):
    return mathx.divide0(y1*(x2 - x) + y2*(x - x1), x2 - x1, float('nan'))


def peak_crossings_1D(x, y, frac=0.5, ym=None):
    """
    Args:
        x: increasing array
        y: function sampled at x
        ym: if supplied, use as maximum instead
    """
    x = np.asarray(x)
    y = np.asarray(y)
    im = y.argmax()
    if ym is None:
        ym = y[im]
    yc = ym*frac
    # after
    ais = im + (y[im:] < yc).nonzero()[0]
    if len(ais) == 0:
        ai = len(x) - 1  # x[-1]
    else:
        ai = ais[0]  # a=x[ai]-x[ai-1]
    a = line_two_points(y[ai - 1], x[ai - 1], y[ai], x[ai], yc)
    # before
    bis = im - (y[im::-1] < ym*frac).nonzero()[0]
    if len(bis) == 0:
        bi = 0
    else:
        bi = min(bis[0], len(x) - 2)
    b = line_two_points(y[bi], x[bi], y[bi + 1], x[bi + 1], yc)
    return b, a


def peak_crossings(x, y, frac=0.5, axis=None, ym=None):
    if axis is None:
        axis = mathx.last_axis(x)
    if ym is None:
        return mathx.eval_iterated(lambda x, y: peak_crossings_1D(x, y, frac), (x, y), vec_dims=[axis])
    else:
        return mathx.eval_iterated(lambda x, y, ym: peak_crossings_1D(x, y, frac, ym), (x, y, ym), vec_dims=[axis])


def fwhm(x, y, axis=None):
    x1, x2 = peak_crossings(x, y, 0.5, axis)
    return x2 - x1


def find_peaks_iter_rmv(y, n, Dy_thresh=0, max_half_int=float('inf'), cyclic=False, min_half_int=-float('inf')):
    """Finds peaks using 'iterative removal'.

    The maximum value is recorded as a peak. Then, an interval
    around this maximum is removed. The interval is defined by the closest local
    minima or max_half_int, whichever is smaller. Local minima are defined by
    y rising from the minimum by Dy_thresh.
    Args:
        y (sequence): vector in which to find peaks
        n (int): number of peaks
        Dy_thresh (float): Minimum increase to declare a local minimum
        max_half_int (float): maximum distance from peak for removal
        cyclic (bool): cyclic boundary conditions
    Returns: the peaks in order of discovery.
        """
    y = y.copy()  # we change it
    min_y = y.min()  # set 'removed' intervals to this

    def find_rmv_peak():
        ind_peak = y.argmax()

        def scan(ind, dir):
            if cyclic:
                stop_ind = None
            else:
                if dir > 0:
                    stop_ind = len(y) - 1
                else:
                    stop_ind = 0
            scan_min_y = y[ind]
            scan_min_ind = ind
            dist = 0
            halt = False
            while ind != stop_ind:
                # Have we risen out of a minimum?
                if y[ind + dir] - scan_min_y > Dy_thresh:
                    halt = True
                if dist >= min_half_int and halt:
                    break
                if dist == max_half_int:
                    break
                ind += dir
                dist += 1
                # Update minimum
                if y[ind] < scan_min_y:
                    scan_min_y = y[ind]
                    scan_min_ind = ind
            return scan_min_ind

        # Set interval to minimum
        left_ind = scan(ind_peak, -1)
        right_ind = scan(ind_peak, 1)
        y[left_ind:right_ind + 1] = min_y
        return ind_peak

    ind_peaks = []
    for _ in range(n):
        ind_peaks.append(find_rmv_peak())
    return ind_peaks


def polar_to_cart(r, theta, phi):
    """Convert from polar to cartesian coordinate system.

    Angles in radians.

    Args:
        r: distance from origin
        theta: angle to z axis
        phi: angle around z axis, starting from x moving towards y

    Returns:
        tuple: x,y,z coordinates
    """
    rs = r*np.sin(theta)
    return rs*np.cos(phi), rs*np.sin(phi), r*np.cos(theta)


def polar_reg_grid_to_rect(r, theta, data, theta_repeats=False, osamp=1):
    """data dimensions are r, theta. r, theta must be (1D) sequences. If theta_repeats then
    an additional theta column is added, equal to the first. This is useful
    if theta runs from e.g. 0, Delta, ..., 2*pi-Delta"""
    assert np.ndim(r) == 1
    assert np.ndim(theta) == 1
    max_r = r[-1]
    x = np.linspace(-max_r, max_r, len(r)*2*osamp)
    y = x[:, None]
    rxy = (x**2 + y**2)**0.5
    thetaxy = np.arctan2(y, x)
    ri = usv.get_frac_ind(r, rxy)
    if theta_repeats:
        theta = np.r_[theta, theta[0] + 2*np.pi*np.sign(theta[1] - theta[0])]  # theta[-1]-theta[-2]]
        data = np.c_[data, data[:, 0]]
    theta0 = min(theta)
    thetai = usv.get_frac_ind(theta, (thetaxy - theta0)%(2*np.pi) + theta0)
    datayx = map_coordinates(data, np.stack((ri, thetai), -3))
    return x, y, datayx


def cart_to_polar(x, y, z, r_sign=1):
    """Convert from cartesian to polar coordinates.

    See polar_to_cart for defintions.
    """
    r = r_sign*(x**2 + y**2 + z**2)**0.5
    theta = np.arccos(mathx.divide0(z, r, 1))
    phi = np.arctan2(y*r_sign, x*r_sign)
    return r, theta, phi


def polar_grid(Ntheta, Nphi, dim_theta=-2, dim_phi=-1):
    theta = np.pi*(mathx.reshape_vec(np.arange(Ntheta), dim_theta) + 1)/(Ntheta + 1)
    phi = np.pi*2*mathx.reshape_vec(np.arange(Nphi), dim_phi)/Nphi
    return theta, phi


def polar_perm_cart(theta, phi, perm):
    xs = polar_to_cart(1, theta, phi)
    xs = [xs[comp] for comp in perm]
    return cart_to_polar(*xs)[1:]


def negate_polar(theta, phi):
    return np.pi - theta, mathx.wrap_pm(phi + np.pi, np.pi)

def find_2d_grid_crossings(nx, ny, ox, oy, vx, vy):
    """Find intersections of line with 2D grid.

    The grid lines are x = 0, 1, ..., nx and y = 0, 1, ..., ny.

    The line is r = o + d*v where o = (ox, oy) and v = (vx, vy).

    Returns:
        1d array: Values of d at which the line crosses a grid line. Increasing order.
    """
    def round_if_close(x):
        if abs(x - round(x)) < 1e-12:
            x = round(x)
        return x
    # Find 'most negative' d.
    d = max(min(np.divide(-ox, vx), np.divide(nx - ox, vx)), min(np.divide(-oy, vy), np.divide(ny - oy, vy)))
    x = ox + vx*d
    y = oy + vy*d
    crossings = [d]
    while True:
        xn = math.floor(x + 1) if vx > 0 else math.ceil(x - 1)
        yn = math.floor(y + 1) if vy > 0 else math.ceil(y - 1)
        ds = np.asarray((np.divide(xn - x, vx), np.divide(yn - y, vy)))
        dd = min(ds[np.isfinite(ds)])
        d += dd
        assert dd > 0
        x = round_if_close(x + vx*dd)
        y = round_if_close(y + vy*dd)
        if x < 0 or x > nx or y < 0 or y > ny:
            break
        crossings.append(d)
    return np.asarray(crossings)