import numpy as np
from mathx import usv

t0 = usv.array(zero=1.5, N=4, delta=1.4, axis=-1)


def test_basics():
    assert (usv.desc(t0) == 'z1.5d1.4N4')
    assert (usv.desc(t0[1:]) == 'z2.9d1.4N3')
    assert (usv.desc(t0[:-1]) == 'z1.5d1.4N3')
    assert (usv.desc(t0[::2]) == 'z1.5d2.8N2')
    assert (usv.kwargs(t0) == {'N': 4, 'zero': 1.5, 'delta': 1.4, 'axis': -1})

    assert (not usv.is_usv([]))
    # scalar isn't a USV
    assert (not usv.is_usv(3))
    assert (usv.is_usv(t0))
    assert (usv.is_usv([1, 2, 3]))
    assert (not usv.is_usv([1, 2, 4]))
    # 2D array, axis not specified, so not a USV
    assert (not usv.is_usv([[1, 2, 3], [2, 3, 4], [4, 5, 6]]))
    # 2D array, USV along -1 ...
    assert (usv.is_usv([[1, 2, 3], [2, 3, 4], [4, 5, 6]], -1))
    # ... but not along -2
    assert (not usv.is_usv([[1, 2, 3], [2, 3, 4], [4, 5, 6]], -2))


def test_pad_sampled():
    x = np.array([3, 4, 5])
    y = x**2
    xp, yp = usv.pad_sampled(x, y, 2, 3, value=2)
    assert (np.allclose(xp, [1, 2, 3, 4, 5, 6, 7, 8]))
    assert (np.allclose(yp, [2, 2, 9, 16, 25, 2, 2, 2]))


def test_crop():
    ##
    x = np.arange(0, 12, 2)
    slc = usv.crop_slice(x, 2, 6)
    assert slc == slice(1, 4)
    assert np.array_equal(x[slc], [2, 4, 6])
    ##
    y = np.arange(len(x))
    assert np.array_equal(usv.crop1d(x, 2, 6, y), [1, 2, 3])
    ##
    slc = usv.crop_slice(x, 2, 6, step=2)
    assert slc == slice(1, 4, 2)
    ##
    slc = usv.crop_slice(x, -10, 12, clip=True)
    assert slc == slice(0, 6)  ##


def test_interp1d():
    assert np.allclose(usv.interp1d([1, 2, 3], [-2, -4, -5], [1.5, 2.5, 0]), [-3, -4.5, 0])


def test_interp2d():
    x = np.arange(10)
    y = np.arange(11)
    z = x[:, None]*y
    assert usv.interp2d(x, y, z, x[3], y[4]) == z[3, 4]
    # The test function matches the interpolation form exactly
    assert usv.interp2d(x, y, z, 3.5, 5.5) == 19.25
    assert usv.interp2d(x, y, z, -10, 0) == 0
    assert usv.interp2d(x, y, z, 15, 15) == 225
    xi = np.random.random((2, 1, 4))
    yi = np.random.random((3, 1))
    assert np.allclose(usv.interp2d(x, y, z, xi, yi), xi*yi)


def test_get_frac_ind():
    assert np.array_equal(usv.get_frac_ind(np.arange(5, 100, 5), 10), 1)
    assert np.array_equal(usv.get_frac_ind(np.arange(5, 100, 5), [10, 12.5]), [1, 1.5])


if __name__ == "__main__":
    test_basics()
    test_pad_sampled()
    test_crop()
    test_interp2d()
    test_get_frac_ind()

# ##
# f=t0**2+[[0],[1]]
# vp,fp=usv.pad_sampled(t0,f,5,10)
# ##
# v2=usv.array(zero=0,delta=1,N=10,axis=-2)
# f2=v2**2
# vp2,fp2=usv.pad_sampled(v2,f2,2,3)


"""
Offcuts from a previous attempt

import numpy as np
import mathx.UniformlySpacedVector as USV
import tempfile,os,pickle

t0=USV(zero=1,N=4,Delta=1.4,dim=-1)
print('t0 =',t0)
print('t0[1:] = ',t0[1:])
print('t0[:-1] = ',t0[:-1])
print('t0[::2 = ',t0[::2])
print('t0+1 = ',t0+1)
filename=os.path.join(tempfile.gettempdir(),'t0.p')
pickle.dump(t0,open(filename,'wb'),2)
t0l=pickle.load(open(filename,'rb'))   
print('t0 pickled and unpickled = ',t0l)

t1=USV(zero=[0,1],last=10,N=5,dim=-2)
print(t1)
print(t1[1:])

t2=USV(zero=[[0],[1]],last=10,N=5,dim=-1)
print(t2)

t3=USV(vector=4+np.arange(7)*3)
print(t3)

t4=USV(vector=4+np.arange(7)*3,dim=-2)
print(t4)
t4.Delta
t4.dim
"""
