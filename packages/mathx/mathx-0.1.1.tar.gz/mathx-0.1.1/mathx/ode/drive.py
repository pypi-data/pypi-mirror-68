from functools import total_ordering
from collections import namedtuple
import heapq,math,logging

logger=logging.getLogger(__name__)

class EventQueue:
    @total_ordering
    class Event:
        def __init__(self,time,func,period):
            self.time=time
            self.func=func
            self.period=period
            
        def __eq__(self,other):
            return (self.time,repr(self.func))==(other.time,repr(other.func))
        
        def __lt__(self,other):
            return (self.time,repr(self.func))<(other.time,repr(other.func))
            
    def __init__(self):
        self.queue=[]
        
    @property
    def next_time(self):
        event=self.next_event
        if event is None:
            return float("inf")
        else:
            return event.time
            
    @property
    def next_event(self):
        if len(self.queue)==0:
            return None
        else:
            return self.queue[0]
            
    def process_next_event(self,*args,**kwargs):
        event=heapq.heappop(self.queue)
        if hasattr(event.func,'__call__'):
            result=event.func(event.time,*args,**kwargs)
        else:
            return event.func
        if event.period is not None:
            heapq.heappush(self.queue,self.Event(event.time+event.period,event.func,event.period))
        return result
        
    def add_event(self,t,func,period=None):
        heapq.heappush(self.queue,self.Event(t,func,period))
    
def go(t,y,step,h=None,t_interp_queue=None,steps_queue=None,t_step_queue=None):
    """
    step accepts t, h, y(t), data where data is from the previous successful step,
    and should return
     y(t+h), ok, h_next, data_next, interp, h_actual (if h=None was passed), terminate
    where ok indicates whether
    the step was sucessful (sufficiently accurate), h_next is the next step size
    and data_next is passsed on to the next step.
    Args:
        steps_queue (EventQueue): events timed by number of steps. Called as the step
            begins.
        t_step_queue (EventQueue): events timed by t. Simulation stops on each
        t_interp_queue (EventQueue): events timed by t. Intra-step interpolation
            is used to obtain y.
    """ 
    max_attempts=10
    if t_interp_queue is None:
        t_interp_queue=EventQueue()
    if steps_queue is None:
        steps_queue=EventQueue()
    if t_step_queue is None:
        t_step_queue=EventQueue()
    steps=0
    data=None
    terminate=False
    interp=None
    h_next_attempt=h
    while not terminate:
        logger.debug('t: %g, steps: %g, h: %g, sum|y|^2: %g',t,steps,h,(abs(y)**2).sum())
        while steps_queue.next_time==steps and not terminate:
            terminate=steps_queue.process_next_event(t,y,h,steps,interp)
        while math.isclose(t_step_queue.next_time,t):
            terminate=t_step_queue.process_next_event(t,y,h,steps)
        if terminate:
            break
        ok=False
        attempts=0
        if h_next_attempt is None:
            if t_step_queue.next_time!=float('inf'):
                h_next_attempt=t_step_queue.next_time-t
            else:
                h_next_attempt=1
        else:
            h_next_attempt=min(h_next_attempt,t_step_queue.next_time-t)
        while not ok:
            h=h_next_attempt
            y_next,ok,h_next_attempt,data_next,interp,h_attempt,terminate=step(t,h,y,data)
            attempts+=1
            if attempts==max_attempts:
                raise ValueError('max attempts!')
        # interp is valid from t to t+h
        while t_interp_queue.next_time<=t+h and not terminate:
            te=t_interp_queue.next_time
            ye=interp(te)
            terminate=t_interp_queue.process_next_event(te,ye,h,steps)
        steps+=1
        t+=h
        y=y_next
        data=data_next
    return t,y,h,steps,data
    
class ListBuilder:
    """Builds lists of arguments to repeatedly called function.
    e.g.
    
    lb=ListBuilder()
    for n in range(3):
        lb(n,n**2,n_cubed=n**3,n_plus_1=n+1)
    print(lb.arg_lists)
    print(lb.kwarg_lists)
    
    gives
    
    [[0, 1, 2], [0, 1, 4]]
    {'n_plus_1': [1, 2, 3], 'n_cubed': [0, 1, 8]}
    
    Useful as a callback for driving ODEs
    """
    def __init__(self):
        self.arg_lists=None
        self.kwarg_lists=None
    def __call__(self,*args,**kwargs):
        if len(args)>0:
            if self.arg_lists is None:
                self.arg_lists=[[arg] for arg in args]
            else:
                for arg_list,arg in zip(self.arg_lists,args):
                    arg_list.append(arg)
        if len(kwargs)>0:
            if self.kwarg_lists is None:
                self.kwarg_lists={key:[value] for key,value in kwargs.items()}
            else:
                for key,value in kwargs.items():
                    self.kwarg_lists[key].append(value)
                    
    