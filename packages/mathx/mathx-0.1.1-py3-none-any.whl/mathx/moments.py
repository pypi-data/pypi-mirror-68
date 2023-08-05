import numpy as np
import mathx as mx

def moment(x, f, n, nrm_fac=None, axis=None):
    """sum[x^n*f]/nrm_fac
    nrm_fac defaults to sum(f)."""
    if nrm_fac is None:
        nrm_fac = f.sum(axis, keepdims=True)
    return mx.squeeze_leading(mx.divide0((x**n*f).sum(axis, keepdims=True), nrm_fac))


def moment2(x, y, f, nx, ny, nrm_fac=None):
    """sum[x^nx*y^ny*f]/nrm_fac"""
    if nrm_fac is None:
        nrm_fac = f.sum()
    return (x**nx*y**ny*f).sum()/nrm_fac

def mean_and_variance(x, f):
    """Calculate mean and variance of a function."""
    nrm_fac = np.sum(f)
    mean = moment(x, f, 1, nrm_fac)
    var = moment(x - mean, f, 2, nrm_fac)
    return mean, var

def mean_and_std(x, f):
    mean, var = mean_and_variance(x, f)
    std = var**0.5
    return mean, std

def mean_and_variance2(x, y, f):
    """2D mean and variance calculation.

    The arguments must be broadcastable.

    Returns:
        tuple: <x>,<y>,<(x-<x>)^2>,<(y-<y>)^2>,<(x-<x>)(y-<y>)>
    """
    nrm_fac = f.sum()
    mx = moment(x, f, 1, nrm_fac=nrm_fac)
    my = moment(y, f, 1, nrm_fac=nrm_fac)
    xp = x - mx
    yp = y - my
    vxx = moment(xp, f, 2, nrm_fac)
    vyy = moment(yp, f, 2, nrm_fac)
    vxy = moment2(xp, yp, f, 1, 1, nrm_fac)
    return mx, my, vxx, vyy, vxy


def diagonalize_2d_covariance(vx2, vy2, vxy):
    """Diagonalize 2D covariance matrix to find principle axes.
    Returns:
        tuple (major,minor,theta): major and minor principle root-mean-square
            lengths, and angle of major axis to x axis.
    """
    # Off-diagonal entries of intertia tensor are negative
    m = np.array([[vx2, vxy], [vxy, vy2]])
    vals, vecs = np.linalg.eig(m)
    order = np.argsort(vals)
    min, maj = vals[order]**0.5
    vecs = vecs[:, order]
    theta = np.arctan2(vecs[1, 1], vecs[0, 1])
    return maj, min, theta