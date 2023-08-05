import numpy as np
import mathx
from mathx.qdht import QDHT

def test_self_trans():
    """Test self-transform of exp(-r**2/2)"""
    N=32 # number of sampled points
    ht=QDHT(N)
    # For same r and k axes
    R=ht.j_Np1**0.5
    r=ht.points(R) # radial sampling points
    k=ht.conj_points(R) # angular waveumber sampling points
    Er=np.exp(-r**2/2) # gaussian beam
    Ek=ht.transform(Er,R) # numerical transform
    assert np.allclose(Er,Ek) # they should be equal
    assert np.isclose(ht.integrate(abs(Er)**2,R),ht.conj_integrate(abs(Ek)**2,R))
    
def test_arb_trans():
    ##
    ht=QDHT(64)
    R=5
    r=ht.points(R)
    k=ht.conj_points(R)
    Er=np.exp(-r**2/2)
    Ek=ht.transform(Er,R)
    Eka=ht.transform_to_arb(Er,R,k)
    assert np.allclose(Ek,Eka)
    Eka=ht.transform_to_arb(Er,R,mathx.reshape_vec(k,-3))
    assert np.allclose(Ek,Eka.squeeze()) and Eka.shape==(64,1,1)
    Era=ht.inv_transform_to_arb(Ek,R,r)
    assert np.allclose(Er,Era)
    
    R=ht.j_Np1**0.5 # for same r & k axes
    r=ht.points(R)
    k=ht.conj_points(R)
    Er=np.exp(-r**2/2)
    Erp=-r*np.exp(-r**2/2)
    Ekp=ht.transform_to_arb(Er,R,k,deriv=1)
    assert np.allclose(Erp,Ekp)  
    ##
    
def test_Parseval():
    ##
    ht=QDHT(128)
    R=2
    Er=np.random.randn(ht.N)
    Ek=ht.transform(Er,R)
    assert np.isclose(ht.integrate(abs(Er)**2,R),ht.conj_integrate(abs(Ek)**2,R))
    ##
def test_wierd_shapes():
    ##
    ht=QDHT(16)
    for shape,axis in (((2,3,16,4,5),-3),((16,),0),((16,),-1),((2,16),-1),((2,16),1),((16,2),0),((16,2),-2)):
        Er=np.ones(shape)
        Ek=ht.transform(Er,axis=axis)
        assert Ek.shape==Er.shape
        ##

if __name__=="__main__":
    test_arb_trans()
    test_self_trans()
    test_Parseval()
    test_wierd_shapes()
   

