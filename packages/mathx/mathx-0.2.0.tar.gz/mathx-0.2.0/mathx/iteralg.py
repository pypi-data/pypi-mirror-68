import numpy as np

def converge_aitken_series(f, n_start=0, f_startm1=0, eps=1e-6, max_iter=-1, min_consec=2):
    """Finds the limit of a series using Aitken acceleration
    an = converge_aitken_series(f, n_start, f_startm1)
    where f(n, fp) returns the nth member of the sequence given the n-1th
    member e.g. to sum series s_n, f = s_n + fp.
    n_start is the first value of n (default 1), f_startm1 is the value of fp
    passed at the start (default 0).
    Args:
        min_consec (int): number of consecutive iterations error must be below eps
            to terminate (for robustness)
    """

    def aitken(x1, x2, x3):
        x1, x2, x3 = np.asarray(x1), np.asarray(x2), np.asarray(x3)
        a = x1 - (x2 - x1)**2/(x3 - 2*x2 + x1)
        a = np.asarray(a)
        inds = np.isnan(a)
        a[inds] = x3[inds]
        inds = np.isinf(a)
        a[inds] = x3[inds]
        return a

    n = n_start
    fnp0 = f(n + 0, f_startm1)
    fnp1 = f(n + 1, fnp0)
    fnp2 = f(n + 2, fnp1)
    an = aitken(fnp0, fnp1, fnp2)
    num_consec = 0
    while n != max_iter:
        n += 1
        anm1 = an
        fnp0 = fnp1
        fnp1 = fnp2
        fnp2 = f(n + 2, fnp1)
        an = aitken(fnp0, fnp1, fnp2)
        err = np.asarray((an - anm1)/an)
        anz = an == 0  # Special case for an=0
        err[anz] = an[anz] - anm1[anz]
        if abs(err).max() < eps:
            num_consec += 1
        else:
            num_consec = 0
        if num_consec == min_consec:
            break
    return an
