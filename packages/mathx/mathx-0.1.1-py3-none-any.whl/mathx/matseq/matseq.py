def dot(x,y=None):
    if y is None:
        y=x
    #if axis is None:
    return sum(xe*ye for xe,ye in zip(x,y))

def mult_mat_mat(*args):
    """Multiply two matrices for any indexable types."""
    if len(args) == 2:
        a, b = args
        return [[sum(ae*be for ae, be in zip(a_row, b_col)) for b_col in zip(*b)] for a_row in a]
    else:
        return mult_mat_mat(args[0], mult_mat_mat(*args[1:]))


def mult_mat_vec(a, b):
    """Multiply matrix times vector for any indexable types."""
    return [sum(ae*be for ae, be in zip(a_row, b)) for a_row in a]


def mult_vec_mat(a, b):
    """Multiply vector times matrix for any indexable types."""
    return [sum(ae*be for (ae, be) in zip(a, b_col)) for b_col in zip(*b)]


def mult_mat_scalar(a, s):
    return [[e*s for e in row] for row in a]

def mean(iterable):
    """x can be any iterable"""
    iterator=iter(iterable)
    value=next(iterator)
    num=1
    for element in iterator:
        num+=1
        # value+=element fails when numpy broadcasting
        value=value+element
    return value/num

def project_onto_plane(x, n):
    """Project x onto plane with normal n."""
    d = dot(x, n)
    return [xc - nc*d for xc, nc in zip(x, n)], d