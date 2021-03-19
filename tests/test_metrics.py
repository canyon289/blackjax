from unittest import mock

import jax.numpy as jnp
from jax import random

import pytest

from blackjax.inference import metrics

KEY = random.PRNGKey(0)
DTYPE = "float32"


def test_gaussian_euclidean_ndim_3():
    """Test Gaussian Euclidean Function returns correct function when ndim > 1"""
    x = jnp.ones(shape=(1, 2, 3))

    with pytest.raises(ValueError) as e:
        metrics.gaussian_euclidean(x)
    assert "The mass matrix has the wrong number of dimensions" in str(e)


def test_gaussian_euclidean_dim_1():
    """Test Gaussian Euclidean Function with ndim 1"""
    inverse_mass_matrix = jnp.asarray([1/4], dtype=DTYPE)
    momentum, kinetic_energy = metrics.gaussian_euclidean(inverse_mass_matrix)

    arbitrary_position = jnp.asarray([12345], dtype=DTYPE)
    momentum_val = momentum(KEY, arbitrary_position)

    # 2 is square root inverse of 1/4
    # -0.20584235 is random value returned with random key
    expected_momentum_val = 2*-0.20584235

    kinetic_energy_val = kinetic_energy(momentum_val)
    velocity = inverse_mass_matrix*momentum_val
    expected_kinetic_energy_val = .5 * velocity * momentum_val

    assert momentum_val == expected_momentum_val
    assert kinetic_energy_val == expected_kinetic_energy_val


def test_gaussian_euclidean_dim_2():
    """Test Gaussian Euclidean Function with ndim 2"""
    inverse_mass_matrix = jnp.asarray([[1/9, 0], [0,1/4]], dtype=DTYPE)
    momentum, kinetic_energy = metrics.gaussian_euclidean(inverse_mass_matrix)

    arbitrary_position = jnp.asarray([12345, 23456], dtype=DTYPE)
    momentum_val = momentum(KEY, arbitrary_position)

    # 2 is square root inverse of 1/4
    # -0.20584235 is random value returned with random key
    expected_momentum_val = jnp.asarray([3,2])* jnp.asarray([-0.784766,  0.8564448])

    kinetic_energy_val = kinetic_energy(momentum_val)
    velocity = jnp.dot(inverse_mass_matrix,momentum_val)
    expected_kinetic_energy_val = .5 * jnp.matmul(velocity, momentum_val)

    assert pytest.approx(expected_momentum_val, momentum_val)
    assert kinetic_energy_val == expected_kinetic_energy_val
