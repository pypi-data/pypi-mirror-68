# TODO turn this into a propoer test
from mathx.ode.drive import *
import numpy as np
from mathx.ode.model_systems import wave
from mathx.ode import rk45
from functools import partial

def test_rk45():
    y_0,soln,f,P=wave()
    y_0=np.array(y_0)
    rtol=1e-4
    t_interp_queue=EventQueue()
    t_interp_queue.add_event(10,True) # stop
    lists=ListBuilder()
    t_interp_queue.add_event(0,lists,0.1)
    steps_queue=EventQueue()
    steps_queue.add_event(0,lambda _,t,y,h,steps,interp:print('#%d t=%.2f h=%s'%(steps,t,'%.3f'%h if h is not None else 'None')),2)
    t_step_queue=EventQueue()
    t_step_queue.add_event(0,lambda _,t,y,h,steps:print('stopping at %.3f'%t),1)
    go(0,y_0,lambda t,h,y,data:rk45.step_precon(t,h,y,f,data,P,rtol),t_interp_queue=t_interp_queue,steps_queue=steps_queue,t_step_queue=t_step_queue)
    t=np.array(lists.arg_lists[0])
    y=np.array(lists.arg_lists[1])

    ##
    lb=ListBuilder()
    for n in range(3):
        lb(n,n**2,n_cubed=n**3,n_plus_1=n+1)
    # print(lb.arg_lists)
    # print(lb.kwarg_lists)
