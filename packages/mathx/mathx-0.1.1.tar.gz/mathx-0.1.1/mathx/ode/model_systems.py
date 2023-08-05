import numpy as np

def constant_force(force=1):
    # Constant force, uniform motion
    y_0=[10.,-10.]
    def soln(t):
        return np.concatenate([force*t**2/2+y_0[1]*t+y_0[0],force*t+y_0[1]],-1)
    def f(t,y):
        return np.array([y[1],force])
    return y_0,soln,f,None
    
def sinusoidal_force():
    # Sinusoidal driving force
    p_0=1.
    v_0=1.
    y_0=[p_0,v_0]
    def f(t,y):
        return np.array([y[1],np.cos(t)])
    def soln(t):
        return np.concatenate([-np.cos(t)+1+p_0+v_0*t,np.sin(t)+v_0],-1)
    return y_0,soln,f,None
    
def wave():
    # Wave with ang. frequency a and source b
    a=1.2
    b=0.5
    y_0=[1+0j]
    def f(t,y):
        return b
    def soln(t):
        return b*(np.exp(1j*a*t)-1)/(1j*a)+y_0*np.exp(1j*a*t)
    def P(t_0,y,t_1):
        return np.exp(1j*a*(t_1-t_0))*y
    return y_0,soln,f,P
    

    