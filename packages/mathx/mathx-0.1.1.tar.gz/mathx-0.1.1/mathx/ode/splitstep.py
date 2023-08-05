"""Functions for solving ODEs with the split-step method.

For all functions, inputs are:
t - start time
y - solution at t in domain 1
h - step size
prop_1(t,y,h) - function which propagates solution in domain 1 from t to t+h
trans(y) - transform solution from domain 1 to 2
prop_2(t,y,h) - same for domain 2
inv_trans(y) - transform from domain 2 to 1
"""    
import numpy as np
import sys
import mathx

def double(t,y,h,prop_1,trans,prop_2,inv_trans):
    y=prop_1(t,y,h*0.25)
    y=trans(y)
    y=prop_2(t,y,h*0.5)
    y=inv_trans(y)
    y=prop_1(t+h*0.25,y,h*0.5)
    y=trans(y)
    y=prop_2(t+0.5*h,y,h*0.5)
    y=inv_trans(y)
    y=prop_1(t+h*0.75,y,h*0.25)
    return y
    
def single(t,y,h,prop_1,trans,prop_2,inv_trans):
    y=prop_1(t,y,h*0.5)
    y=trans(y)
    y=prop_2(t,y,h)
    y=inv_trans(y)
    y=prop_1(t+h*0.5,y,h*0.5)
    return y
    
def double_check(t,y,h,prop_1,trans,prop_2,inv_trans):
    yd=double(t,y,h,prop_1,trans,prop_2,inv_trans)
    ys=single(t,y,h,prop_1,trans,prop_2,inv_trans)
    return yd,ys
    
def adaptive(t,y,h,prop_1,trans,prop_2,inv_trans,err_tol=1e-3,err_fun=None):
    if err_fun is None:
        err_fun=lambda yd,ys: (mathx.abs_sqd(yd-ys).sum()/mathx.abs_sqd(yd).sum())**0.5
    yd=double(t,y,h,prop_1,trans,prop_2,inv_trans)
    ys=single(t,y,h,prop_1,trans,prop_2,inv_trans)
    
    # Per channel - maybe TODO make option
    #rel_err=(abs(yd-ys)/np.maximum(np.maximum(abs(yd),abs(ys)),sys.float_info.min)).max()
    err=err_fun(yd,ys)
    eps=err_tol/err
    pow=1./3
    ok=eps>=1
    if eps>=1:
        h_next=h*min(0.9*eps**pow,10)  
    else:
        h_next=h*max(0.9*eps**pow,0.1)
    return yd,ok,h_next,None,None,h,False
        
