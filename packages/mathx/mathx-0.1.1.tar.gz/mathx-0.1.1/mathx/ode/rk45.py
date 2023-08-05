"""Runge-Kutta 4,5 ('Dormand-Prince' method, ode45 in MATLAB) solution to ODEs.
"""
import mathx
from mathx import abs_sqd, matseq
import numpy as np
from numpy import maximum, zeros, array, cumprod
import sys

# fractions of h for step evaluation
H = [1./5, 3./10, 4./5, 8./9, 1, 1]

# Butcher tableau
F = [[1./5], [3./40, 9./40], [44./45, -56./15, 32/9.], [19372./6561, -25360./2187, 64448./6561, -212./729],
     [9017./3168, -355./33, 46732./5247, 49./176, -5103./18656], [35./384, 0, 500./1113, 125./192, -2187./6784, 11./84]]

# Error estimate
E = [71./57600, 0, -71./16695, 71./1920, -17253./339200, 22./525, -1./40]

# Interpolation matrix
I = [[1, -183./64, 37./12, -145./128], [0, 0, 0, 0], [0, 1500./371, -1000./159, 1000./371],
     [0, -125./32, 125./12, -375./64], [0, 9477./3392, -729./106, 25515./6784], [0, -11./7, 11./3, -55./28],
     [0, 3./2, -4, 5./2]]


def step(t, h, y, f, f0=None, rtol=1e-4):
    """Take a single step RK45 step and evaluate accuracy.
    
    Arguments:
    t - time of start of step
    h - step size
    y - solution at start of step
    f - derivative function f(t,y)
    f0 - f evaluated at t, None if unknown
    rtol - step tolerance 
    
    Returns tuple of:
    yn - y at t+h
    ok - whether error was below tolerance
    hn - new step size
    f(t+h,yn) - last function evaluation
    interpolation object
    h - used step size
    False - whether to terminate
    """
    pow = 1./5
    # Use first same as last (FSAL) property. This makes 6 evaluations per step.
    if f0 is None:
        f0 = f(t, y)
    if h is None:
        h = max((abs(y)/maximum(abs(f0), sys.float_info.min)).min(), sys.float_info.min)
    fe = [f0]  # = evaluations of f(t,y)
    for n in range(1, 7):
        yp = y + h*matseq.dot(fe, F[n - 1])
        if n == 6:
            yn = yp
        fe.append(f(t + h*H[n - 1], yp))
    f_err = matseq.dot(fe, E)
    # err = abs(h)*max(abs(f_err)/maximum(abs(y),abs(yn)))
    err = abs(h)*np.max(abs(f_err))/np.max(np.maximum(abs(y), abs(yn)))
    ok = err <= rtol
    if ok:
        temp = 1.25*(err/rtol)**pow;
        if temp > 0.2:
            hn = h/temp
        else:
            hn = 5.0*h
    else:
        hn = h*max(0.1, 0.8*(rtol/err)**pow)

    return yn, ok, hn, fe[-1], Interp(t, h, y, fe), h, False


def interp_step(t, h, y, fe, ti):
    """Interpolate RK45 solution using function evaluations.
    
    t - start of time step
    h - step size
    y - solution at t
    ti - time to integrate to
    fe - derivative function evaluations from rk45.step
    
    returns - y at t
    """
    s = [(ti - t)/h]
    for n in range(3):
        s.append(s[-1]*s[0])
    return y + h*matseq.dot(fe, matseq.mult_mat_vec(I, s))


class Interp:
    def __init__(self, t, h, y, fe):
        self.t = t
        self.h = h
        self.y = y
        self.fe = fe

    def __call__(self, ti):
        return interp_step(self.t, self.h, self.y, self.fe, ti)


class InterpPrecon(Interp):
    def __init__(self, interpb, P):
        Interp.__init__(self, interpb.t, interpb.h, interpb.y, interpb.fe)
        self.P = P

    def __call__(self, ti):
        return self.P(self.t, interp_step(self.t, self.h, self.y, self.fe, ti), ti)


def step_precon(t, h, y, f, f0, P, rtol=1e-4):
    """Takes an RK45 step of dy/dt = L(t)y + f(t, y) from t to t+h. 
    Uses transformation p95
     RT4. P(t_0,y_0,t_1)=exp(int_{t_0}^{t_1}L(t)dt)y_0 is the propagator
     corresponding to L
     """

    # We use 'barred' variables
    # yb = y exp(-int_{t}^tp L)
    def eval_f(tp, yb):
        """Compute derivative function given yb at tb."""
        # Transform from yb to y
        y = P(t, yb, tp)
        # Evaluate derivative
        fe = f(tp, y)
        # Transform back
        fb = P(tp, fe, t)
        return fb

    # Take the step in yb (y bar) space. At t, y=yb
    ybn, ok, hn, fb7, interpb, h, terminate = step(t, h, y, eval_f, f0, rtol)
    # Linearly propagate to t+h
    yn = P(t, ybn, t + h)
    f7 = P(t, fb7, t + h)
    interp = InterpPrecon(interpb, P)
    return yn, ok, hn, f7, interp, h, terminate

# def integrate(t_0,y,step):


#     

# 
# def step(t,h,y,f,f0=None,rtol=1e-4):
#     """Take a single step of the Runge-Kutta 4,5 method.
#     This is the 'Dormand-Prince' method:
#     http://en.wikipedia.org/wiki/Dormand%E2%80%93Prince_method. In MATLAB it is
#     ode45."""
#     pow = 1/5
#     # Use first same as last (FSAL) property. This makes 6 evaluations per step.
#     if f0==None:
#         f0=f(t,y)
#     fe=zeros((7,)+f0.shape)
#     for n in range(1,6):
#         yp=y+tensordot(fe[0:n,...],F[:n,n-1],(1,1))
#         if n==6:
#             yn=yp
#         fe[n,...]=f(t+h*H[n-1],yp)
#     f_err=tensordot(fe,E,(1,1))
#     err = h*(f_err/(maximum(abs_sqd(y),abs_sqd(yn)).max()**0.5)).max()
#     ok = err <= rtol
#     if ok:
#         temp = 1.25*(err/options.rtol)^pow;
#         if temp > 0.2:
#             hn = h / temp
#         else:
#             hn = 5.0*h
#     else:
#         hn = h * max(0.1, 0.8*(options.rtol/err)^pow)
# 
# 
#     
# def step(t, h, y, f, f1=None, rtol=1e-4):
#     """Take a single step of the Runge-Kutta 4,5 method.
#     This is the 'Dormand-Prince' method:
#     http://en.wikipedia.org/wiki/Dormand%E2%80%93Prince_method. In MATLAB it is
#     ode45."""
#     pow = 1/5
#     # Use first same as last (FSAL) property. This makes 6 evaluations per step.
#     if f1==None:
#         f1=f(t,y)
#     f2 = f(t + h*1/5,       y + f1*(h*1/5))
#     f3 = f(t + h*3/10,      y + f1*(h*3/40)       + f2*(h*9/40))
#     f4 = f(t + h*4/5,       y + f1*(h*44/45)      - f2*(h*56/15)      + f3*(h*32/9))
#     f5 = f(t + h*8/9,       y + f1*(h*19372/6561) - f2*(h*25360/2187) + f3*(h*64448/6561) - f4*(h*212/729))
#     f6 = f(t + h,           y + f1*(h*9017/3168)  - f2*(h*355/33)     + f3*(h*46732/5247) + f4*(h*49/176)  - f5*(h*5103/18656))
#     yn =                    y + f1*(h*35/384)                         + f3*(h*500/1113)   + f4*(h*125/192) - f5*(h*2187/6784) + f6*(h*11/84)
#     f7 = f(t + h,           yn)
#     fE = f1*(71/57600) - f3*(71/16695) + f4*(71/1920) - f5*(17253/339200) + f6*(22/525) - f7*(1/40)
#     err = h*(fE/(maximum(abs_sqd(y),abs_sqd(yn)).max()**0.5)).max()
#     ok = err <= rtol
#     if ok:
#         temp = 1.25*(err/options.rtol)^pow;
#         if temp > 0.2:
#             hn = h / temp
#         else:
#             hn = 5.0*h
#     else:
#         hn = h * max(0.1, 0.8*(options.rtol/err)^pow)
#     def interp(ti):
#         M=[ [1,       -183/64,      37/12,       -145/128],
#             [0,       0,            0            0],
#             [0        1500/371,     -1000/159,   1000/371],
#             [0,       -125/32,      125/12,      -375/64],
#             [0,       9477/3392,    -729/106,    25515/6784],
#             [0,       -11/7,        11/3,        -55/28],
#             [0,       3/2,          -4,           5/2]]
#         s=[(ti-t)/h]
#         for n in range(3):
#             s.append(s[-1]*s[0])
#         mult_vec_mat(f,mult_mat_vec(M,s))
#         
#     
#     
#     return yn,ok,hn,f7
