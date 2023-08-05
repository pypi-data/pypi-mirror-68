import numpy as np
from mathx import matseq

def test_mean():
    assert matseq.mean([1, 2, 3]) == 2
    assert matseq.mean([1]) == 1
    assert np.array_equal(matseq.mean([np.array([1, 2]), np.array([1, 2])[:, None]]), np.array([[1, 1.5], [1.5, 2]]))
