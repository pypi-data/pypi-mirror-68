import numpy as np

def cosine_apod(t, t_0, Dt):
    """If Dt>0, one for t<t_0, cosine from t_0 to t_0+Dt, zero for t>t_0+Dt.
    If Dt<0, one for t>t_0, cosine from t_0 to t_0+Dt, zero for t<t0+Dt."""
    return np.cos(np.maximum(np.minimum((t - t_0)/Dt, 1), 0)*np.pi/2)**2


def cosine_window(t, t1, t2, Dt1, Dt2=None):
    """0 in t<(t1-Dt) and t>(t2+Dt), 1 in t1<t<t2, cosine transitions."""
    t = np.asarray(t)
    if Dt2 is None:
        Dt2 = Dt1
    # return np.cos(np.minimum(np.maximum(np.maximum(t-t2,t1-t)/Dt,0),1)*math.pi/2)**2
    return np.cos(np.minimum(np.maximum(np.maximum((t1 - t)/Dt1, (t - t2)/Dt2), 0), 1)*np.pi/2)**2


def xcorr_fft_2d(a, b, a_ft=False, b_ft=False, shift=True):
    """Compute cross-correlation between two 2D arrays of equal shape by using fourier transform
    (uses convolution theorem with an extra conjugate).
    Can supply pre-calculated fts of a and/or b. If so, set a_ft and/or b_ft to True"""
    if a.shape != b.shape:
        raise ValueError('Both input arrays must have the same shape - got {0} and {1}.'.format(a.shape, b.shape))
    afft = (a if a_ft else np.fft.fft2(a))
    bfft = (b if b_ft else np.fft.fft2(b))
    xc = np.fft.ifft2(afft*np.conj(bfft))
    if shift:
        xc = np.fft.fftshift(xc)
    return xc


def xcorr_fft_1d(a, b, a_ft=False, b_ft=False, shift=True):
    """Compute cross-correlation between two 1D arrays of equal shape by using fourier transform
    (uses convolution theorem with an extra conjugate).
    Can supply pre-calculated fts of a and/or b. If so, set a_ft and/or b_ft to True"""
    if a.shape != b.shape:
        raise ValueError('Both input arrays must have the same shape - got {0} and {1}.'.format(a.shape, b.shape))
    afft = (a if a_ft else np.fft.fft(a))
    bfft = (b if b_ft else np.fft.fft(b))
    xc = np.fft.ifft(afft*np.conj(bfft))
    if shift:
        xc = np.fft.fftshift(xc)
    return xc

def thresholded(y,fraction_max=None,level=None):
    if level is not None:
        assert fraction_max is None
    else:
        level=y.max()*fraction_max
    y=y.copy()
    y[y<level]=0
    return y