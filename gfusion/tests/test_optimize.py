"""Test for optimize module"""
import numpy as np
from numpy.testing import assert_array_equal
from nose.tools import assert_equal
from ..optimize import simplex_projection


def test_simplex_projection():
    # values on a simplex should not be modified
    simplex_vectors = [
        [0.3, 0.4, 0.3],
        np.ones(5)/5,
    ]
    for y in simplex_vectors:
        x = simplex_projection(y)
        assert_array_equal(x, y)
