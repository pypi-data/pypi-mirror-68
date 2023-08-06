"""Tests for schmidt_decomposition function."""
import unittest
import numpy as np

from toqito.states import max_entangled
from toqito.state_ops import schmidt_decomposition


class TestSchmidtDecomposition(unittest.TestCase):

    """Unit tests for schmidt_decomposition."""

    def test_schmidt_decomp_max_ent(self):
        """Schmidt decomposition of the 3-D maximally entangled state."""
        singular_vals, u_mat, vt_mat = schmidt_decomposition(max_entangled(3))

        expected_u_mat = np.identity(3)
        expected_vt_mat = np.identity(3)
        expected_singular_vals = 1 / np.sqrt(3) * np.array([[1], [1], [1]])

        bool_mat = np.isclose(expected_u_mat, u_mat)
        self.assertEqual(np.all(bool_mat), True)

        bool_mat = np.isclose(expected_vt_mat, vt_mat)
        self.assertEqual(np.all(bool_mat), True)

        bool_mat = np.isclose(expected_singular_vals, singular_vals)
        self.assertEqual(np.all(bool_mat), True)


if __name__ == "__main__":
    unittest.main()
