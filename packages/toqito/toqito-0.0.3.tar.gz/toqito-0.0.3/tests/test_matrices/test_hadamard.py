"""Tests for hadamard function."""
import unittest
import numpy as np

from toqito.matrices import hadamard


class TestHadamard(unittest.TestCase):

    """Unit test for hadamard."""

    def test_hadamard_0(self):
        """Test for Hadamard function when n = 0."""
        res = hadamard(0)
        expected_res = np.array([[1]])
        bool_mat = np.isclose(res, expected_res)
        self.assertEqual(np.all(bool_mat), True)

    def test_hadamard_1(self):
        """Test for Hadamard function when n = 1."""
        res = hadamard(1)
        expected_res = 1 / np.sqrt(2) * np.array([[1, 1], [1, -1]])
        bool_mat = np.isclose(res, expected_res)
        self.assertEqual(np.all(bool_mat), True)

    def test_hadamard_2(self):
        """Test for Hadamard function when n = 2."""
        res = hadamard(2)
        expected_res = (
            1
            / 2
            * np.array([[1, 1, 1, 1], [1, -1, 1, -1], [1, 1, -1, -1], [1, -1, -1, 1]])
        )
        bool_mat = np.isclose(res, expected_res)
        self.assertEqual(np.all(bool_mat), True)

    def test_hadamard_3(self):
        """Test for Hadamard function when n = 3."""
        res = hadamard(3)
        expected_res = (
            1
            / (2 ** (3 / 2))
            * np.array(
                [
                    [1, 1, 1, 1, 1, 1, 1, 1],
                    [1, -1, 1, -1, 1, -1, 1, -1],
                    [1, 1, -1, -1, 1, 1, -1, -1],
                    [1, -1, -1, 1, 1, -1, -1, 1],
                    [1, 1, 1, 1, -1, -1, -1, -1],
                    [1, -1, 1, -1, -1, 1, -1, 1],
                    [1, 1, -1, -1, -1, -1, 1, 1],
                    [1, -1, -1, 1, -1, 1, 1, -1],
                ]
            )
        )
        bool_mat = np.isclose(res, expected_res)
        self.assertEqual(np.all(bool_mat), True)

    def test_hadamard_negative(self):
        """Input must be non-negative."""
        with self.assertRaises(ValueError):
            hadamard(-1)


if __name__ == "__main__":
    unittest.main()
