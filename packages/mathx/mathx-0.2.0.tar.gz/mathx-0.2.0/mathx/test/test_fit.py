import numpy as np
import mathx as mx

def test_fit_sparse_1d_poly():
    ##
    x=np.linspace(-50,50)
    y=np.linspace(-60,60,100)[:,None]
    x0=5
    y0=2
    sx=4
    sy=3
    
    pows=[1,0,2]
    def test(cs):
        p=sum(c*x**pow for c,pow in zip(cs,pows))
        z=np.exp(-0.5*((x/sx)**2+((y-p)/sy)**2))    
        cs_fit=mx.fit_sparse_1d_poly(x,y,z,pows)
        assert np.allclose(cs_fit,cs)
    test([0.1,2,0.1])
    test([1,0,0])
    test([-1,0,0])
    test([0,0,0])
    test([0,10,0])
    test([0,10,-0.1])
    ##
test_fit_sparse_1d_poly()