import _matrix
import pytest
import random
import unittest

class Test_Matrix(unittest.TestCase):
    def make_matrices(self, size):

        mat1 = _matrix.Matrix(size,size)
        mat2 = _matrix.Matrix(size,size)
        mat3 = _matrix.Matrix(size,size)

        for it in range(size):
            for jt in range(size):
                mat1[it, jt] = it * size + jt + 1
                mat2[it, jt] = it * size + jt + 1
                mat3[it, jt] = 0

        return mat1, mat2, mat3

    def test_init(self):
        size = 5
        mat = _matrix.Matrix(size, size)
        assert mat.nrow == size
        assert mat.ncol == size
        assert mat.getVector() == [0] * size * size
    
    def test_multiply(self):
        mat1 = _matrix.Matrix(2, 3, [1, 2, 3, 4, 5, 6])
        mat2 = _matrix.Matrix(3, 2, [7, 8, 9, 10, 11, 12])
        navi_result = _matrix.multiply_naive(mat1, mat2)
        tile_result = _matrix.multiply_tile(mat1, mat2, 2)
        mkl_result = _matrix.multiply_mkl(mat1, mat2)
        expected = [58, 64, 139, 154]
        assert navi_result.getVector() == expected
        assert tile_result.getVector() == expected
        assert mkl_result.getVector() == expected
    
    def test_zero(self):
        size = 100
        mat1, mat2, mat3, *_ = self.make_matrices(size)

        ret_naive = _matrix.multiply_naive(mat1, mat3)
        ret_mkl = _matrix.multiply_mkl(mat1, mat3)

        assert size == ret_naive.nrow
        assert size == ret_naive.ncol
        assert size == ret_mkl.nrow
        assert size == ret_mkl.ncol

        for i in range(ret_naive.nrow):
            for j in range(ret_naive.ncol):
                assert 0 == ret_naive[i, j]
                assert 0 == ret_mkl[i, j]