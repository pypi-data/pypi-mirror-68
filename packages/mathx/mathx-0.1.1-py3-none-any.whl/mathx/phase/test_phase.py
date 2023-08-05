"""Stationary phase approximations"""
import numpy as np

import mathx as mx
from mathx import sft, phase

k = np.linspace(-20, 20, 1000)
gk = np.exp(-0.5*k**2)
fk = 2*np.exp(-0.5*(k - 1)**2 + 1.5j)

x = sft.conj_axis(k)
ftd = sft.FTD(x=x, k=k)
g = ftd.inv_trans(gk)
f = ftd.inv_trans(fk)


def test_optimal_linear_phase():
    assert np.allclose(phase.optimal_linear_phase(x, f*g.conj()), [1, 1.5])


def test_straight_line_phase_scale():
    fp = phase.apply_straight_line_phase_scale(x, f, g)
    assert (abs(fp - g)**2).sum() < 1e-10


def test_unwrap_paint_fill():
    x = np.linspace(-10, 10, 10)
    y = np.linspace(-10, 10, 11)[:, None]
    z = np.linspace(-10, 10, 12)[:, None, None]
    rsqd = x**2 + y**2 + z**2
    phi_uw = rsqd/30
    phi_w = mx.wrap_to_pm(phi_uw, np.pi)
    w = np.exp(-rsqd/300)
    phi_p = phi_w.copy()
    phase.unwrap_paint_fill(phi_p, w)
    assert np.allclose(phi_uw, phi_p)


def test_unwrap_axes():
    x = np.linspace(-10, 10, 10)
    y = np.linspace(-10, 10, 11)[:, None]
    # z=np.linspace(-10,10,12)[:,None,None]
    z = 0
    rsqd = x**2 + y**2 + z**2
    phi_uw = rsqd/30
    phi_w = mx.wrap_to_pm(phi_uw, np.pi)
    w = np.exp(-rsqd/300)
    raveled_index = w.argmax()
    phi_p = phase.unwrap_axes(phi_w, raveled_index, [-2, -1])
    assert abs(mx.wrap_to_pm(phi_p - phi_w, np.pi)).max() < 1e-6
    index = np.unravel_index(raveled_index, w.shape)
    assert abs(np.diff(phi_p, axis=-2)).max() < np.pi
    assert abs(np.diff(phi_p, axis=-1)).max() < np.pi
    assert np.allclose(phi_uw, phi_p)


##
def test_approximate_phase_inflexion():
    ## Zero derivative
    g0 = 2
    g1 = 0
    S0 = 4
    S1 = 5
    S3 = 6
    w = 10
    t = np.linspace(-50, 50, 5000000)
    S = S0 + S1*t + S3*t**3/6
    f = (g0 + g1*t)*np.exp(1j*S - 0.5*(t/w)**2)
    intf_num = np.trapz(f, t)
    intf_spa = phase.approximate_phase_inflexion(g0, g1, S0, S1, S3)
    assert np.isclose(intf_num, intf_spa, rtol=1e-2)
    ##
    g0 = 0
    g1 = 2
    S0 = 4
    S1 = 5
    S3 = 6
    w = 10
    t = np.linspace(-50, 50, 5000000)
    S = S0 + S1*t + S3*t**3/6
    f = (g0 + g1*t)*np.exp(1j*S - 0.5*(t/w)**2)
    intf_num = np.trapz(f, t)
    intf_spa = phase.approximate_phase_inflexion(g0, g1, S0, S1, S3)
    assert np.isclose(intf_num, intf_spa, rtol=1e-2)


def test_integrate_quadratic_phase():
    ##
    def ffun(x):
        # Offset Gaussian
        return np.exp(-((x - 1)/1)**2)

    xc = np.linspace(-5, 7)  # Coarse mesh
    fc = ffun(xc)
    xf = np.linspace(-5, 7, 20000)  # Fine mesh
    ff = ffun(xf)
    # Test a range of values for alpha - can even do positive imaginary numbers
    for alpha in (-0.1, 0.1, -1, 1, 5, -5, -50, 50, -100, 100, 1j, 50j, 2j - 50):
        rc = phase.integrate_quadratic_phase(xc, fc, alpha)
        yf = ff*np.exp(1j*alpha*xf**2/2)
        rf = yf.sum()*(xf[1] - xf[0])
        assert np.isclose(rc, rf)
