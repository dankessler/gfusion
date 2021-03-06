"""Tests for main.py"""
from ..main import _solve_weight_vector, _solve_theta
import numpy as np
from numpy.testing import assert_array_almost_equal, assert_array_equal
from nose.tools import assert_raises, assert_equal, assert_true
from scipy import linalg


def test_solve_weight_vector():
    # smoke test
    n_nodes = 4
    n_communities = 2
    n_similarities = 3
    delta = 0.3
    similarities = np.random.random((n_similarities,
                                     n_nodes * (n_nodes-1)/2)) * 10
    grouping_matrix = np.random.random((n_nodes, n_communities))

    weight = _solve_weight_vector(similarities, grouping_matrix, delta)
    assert_equal(weight.ndim, 2)
    assert_equal(weight.shape[1], n_similarities)
    assert_true(np.all(weight >= 0))

    # check raises
    assert_raises(ValueError,
                  _solve_weight_vector, similarities, grouping_matrix, -1)
    similarities_invalid = similarities.copy()
    similarities_invalid[0, 3] = -4.
    assert_raises(ValueError,
                  _solve_weight_vector, similarities_invalid,
                  grouping_matrix, delta)

    # if I have two similarities, and one is null + the grouping matrix is all
    # to all, and delta is not 0, then I expect that
    # the weight vector is [1, 0]
    similarities = np.vstack((1000*np.ones((1, 6)),
                              np.zeros((1, 6))
                              ))
    grouping_matrix = np.ones((4, 4))
    delta = 1
    assert_array_almost_equal(np.atleast_2d([1., 0.]),
                              _solve_weight_vector(similarities,
                                                   grouping_matrix,
                                                   delta))
    # and if I have identical similarities, then it should be .5
    similarities = np.vstack((np.ones((1, 6)),
                              np.ones((1, 6))
                              ))
    grouping_matrix = np.ones((4, 4))
    delta = 1
    assert_array_almost_equal(np.atleast_2d([.5, .5]),
                              _solve_weight_vector(similarities,
                                                   grouping_matrix,
                                                   delta))


def test_solve_theta():
    U = V = L = np.zeros((2, 2))
    R = np.ones((2, 2))

    assert_array_equal(_solve_theta(U, V, L, R), R)

    # test in another way
    for i in range(10):
        n = np.random.randint(1, 10)
        m = np.random.randint(1, 10)
        theta = np.random.randn(n, m)
        R = np.ones((n, m))
        R[0, 0] = 0
        U, L, V = linalg.svd(theta)
        L = linalg.diagsvd(L, *R.shape)
        V = V.T

        theta_ = _solve_theta(U, V, L, R)
        assert_array_almost_equal(theta_[0, 0], theta[0, 0])
        assert_array_equal(theta_.ravel()[1:], R.ravel()[1:])
