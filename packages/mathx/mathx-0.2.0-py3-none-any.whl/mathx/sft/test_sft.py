# TODO: resurrect the tests with plotting, commented out below, in a civilized fashion
# import dill
import pickle
import numpy as np
from mathx.sft import FTD, trans


def test_FTD_0():
    for iter in range(10):
        N = np.random.randint(2, 101)
        ft = FTD(N=N, Dx=np.random.rand(), x_0=np.random.rand(), k_0=np.random.rand())
        y = np.random.rand(np.random.randint(3), N)
        yt = ft.trans(y)
        y2 = np.real(ft.inv_trans(yt))
        np.testing.assert_allclose(y2, y)


def test_FTD_1():
    # Test having a vector for Dx (dim=-1) transforming along dim=-2
    f = FTD(N=10, Dx=(1, 2), x_0=2, k_0=5, axis=-2)
    y = np.arange(10)[:, np.newaxis]
    yp = np.real(f.inv_trans(f.trans(y)))
    assert np.allclose(yp, yp)
    # And likewise for Dk
    f = FTD(N=10, Dk=(1, 2), x_0=2, k_0=5, axis=-2)
    y = np.arange(10)[:, np.newaxis]
    yp = np.real(f.inv_trans(f.trans(y)))
    assert np.allclose(yp, yp)
    # And for x_0
    f = FTD(N=10, Dx=2, x_0=np.array((1, 2, 3)).reshape(-1, 1), k_0=5, axis=-1)
    y = np.arange(10)
    yp = np.real(f.inv_trans(f.trans(y)))
    assert np.allclose(yp, yp)


def test_self_transform():
    ##
    N = 1e2
    # For Dx=Dk
    Dx = (2*np.pi/N)**0.5
    x = (np.arange(N) - N/2)*Dx
    Ex = np.exp(-0.5*x**2)
    Ek = trans(x, -1, Ex, x)
    assert np.allclose(Ek, Ex)  ##


def test_comparison():
    ##
    f = FTD(N=10, Dx=1.5)
    assert f == f
    assert not f != f
    g = FTD(N=10, Dx=1.5, x_0=1)
    assert f != g
    assert not f == g
    g = FTD(N=10, Dx=1.5, k_0=1)
    assert f != g
    assert not f == g


def test_pickling():
    f = FTD(N=10, x_0=[1, 2], Dx=[[1], [2], [3]], k_0=[[[1]], [[2]], [[3]], [[4]]], axis=-4)
    # fp=dill.loads(dill.dumps(f))
    fp = pickle.loads(pickle.dumps(f))
    assert f == fp


if __name__ == "__main__":
    test_FTD_0()
    test_FTD_1()
    test_self_transform()
    test_comparison()

    # import matplotlib.pyplot as plt  # def plot_pulse(t,Et,omega,Ew):  #     plt.figure()  #     plt.subplot(2,1,1)  #     plt.plot(omega,np.abs(Ew)**2)  #     plt.xlabel('omega')  #     plt.subplot(2,1,2)  #     plt.plot(t,np.real(Et))  #     plt.xlabel('t')

#   #   def auto_test(test_num):
#     print('test number %d'%test_num)
#     if test_num==0:
#
#     elif test_num==1:
#         xs=[np.arange(3),mx.reshape_vec(np.arange(4),-2)]
#         ks=[mx.reshape_vec(np.arange(10),-5),mx.reshape_vec(np.arange(11),-6)]
#         trans_to_arb_ND(xs,[-1,-1],np.random.random((5,4,3)),ks,[-1,-2])
#     elif test_num==2:
#
#     else:
#         raise ValueError('Unknown test %d'%test_num)
#
# def plotting_test(test_num):
#     if test_num==0:
#         omega=np.linspace(0.5,4.5,100)
#         T_0=10
#         omega_0=2.35
#         Ef=np.exp(-0.5*((omega-omega_0)*T_0)**2)
#         ft=FTD(k=omega,sign=1,x_m=0)
#         t=ft.x
#         Et=ft.inv_trans(Ef)
#         plot_pulse(t,Et,omega,Ef)
#
#         Et=np.exp(-1j*omega_0*t-0.5*(t/T_0)**2)
#         Ef=ft.trans(Et)
#         plot_pulse(t,Et,omega,Ef)
#
#         Ef=np.exp(-0.5*((omega-omega_0)*T_0)**2)
#         t=np.linspace(-40,40,500)
#         Et=ft.inv_trans_arb(Ef,t)
#         plot_pulse(t,Et,omega,Ef)
#
#         plt.show()
#     elif test_num==1:
#         # test trans_to_arb_ND
#         t=np.linspace(-10,10)
#         t_0=np.linspace(-3,3,10)[:,None]
#         Et=np.exp(-0.5*(t-t_0)**2)
#         omega=conj_axis(t)+np.linspace(-3,3,15)[:,None,None]
#         Ef=trans_to_arb_ND([t],[-1],Et,[omega],[-1])
#         s=3
#         m=14
#         plot_pulse(t,Et[s,:],omega[m,0,:],Ef[m,s,:])
#         plt.show()
#     elif test_num==2:
#         #%%
#         t=np.linspace(-100,100,512)
#         omega=conj_axis(t)
#         omega_0=2.35
#         Et=np.exp(-(t/40)**2-1j*(omega_0+0.02*t)*t)
#         (t_s,omega_s,S)=spectrogram(t,1,Et,40,omega)
#         plt.figure()
#         plt.imshow(S,extent=(np.asscalar(t_s[0]),np.asscalar(t_s[-1]),np.asscalar(omega_s[0]),np.asscalar(omega_s[-1])),origin='lower',aspect='auto',interpolation='none')
#     else:
#         raise ValueError('Unknown test %d'%test_num)
#
# for test_num in range(3):
#     auto_test(test_num)
