import numpy as np
import mathx as mx

def test_windows():
    assert np.allclose(mx.cosine_window([-10, 1, 1.5, 2, 2.5, 3, 4, 5, 10], 2, 3, 1, 2),
                       [0, 0, 0.5, 1, 1, 1, 0.5, 0, 0])