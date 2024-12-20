import _matrix
import pytest
import random
import unittest
import os
import timeit
def test_correctness():
    size =500
    m1 = _matrix.Matrix(size, size)
    m2 = _matrix.Matrix(size, size)

    m3_naive = _matrix.multiply_naive(m1, m2)
    m3_tile = _matrix.multiply_tile(m1, m2, 32)
    m3_mkl = _matrix.multiply_mkl(m1, m2)
    assert m3_tile == m3_naive
    assert m3_mkl == m3_naive
                
class GradingTest(unittest.TestCase):

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

    def test_basic(self):

        size = 100
        mat1, mat2, mat3, *_ = self.make_matrices(size)

        self.assertEqual(size, mat1.nrow)
        self.assertEqual(size, mat1.ncol)
        self.assertEqual(size, mat2.nrow)
        self.assertEqual(size, mat2.ncol)
        self.assertEqual(size, mat3.nrow)
        self.assertEqual(size, mat3.ncol)

        self.assertEqual(2, mat1[0,1])
        self.assertEqual(size+2, mat1[1,1])
        self.assertEqual(size*2, mat1[1,size-1])
        self.assertEqual(size*size, mat1[size-1,size-1])

        for i in range(mat1.nrow):
            for j in range(mat1.ncol):
                self.assertNotEqual(0, mat1[i,j])
                self.assertEqual(mat1[i,j], mat2[i,j])
                self.assertEqual(0, mat3[i,j])

        self.assertEqual(mat1, mat2)
        self.assertTrue(mat1 is not mat2)

    def test_match_naive_mkl(self):

        size = 100
        mat1, mat2, *_ = self.make_matrices(size)

        ret_naive = _matrix.multiply_naive(mat1, mat2)
        ret_mkl = _matrix.multiply_mkl(mat1, mat2)

        self.assertEqual(size, ret_naive.nrow)
        self.assertEqual(size, ret_naive.ncol)
        self.assertEqual(size, ret_mkl.nrow)
        self.assertEqual(size, ret_mkl.ncol)

        for i in range(ret_naive.nrow):
            for j in range(ret_naive.ncol):
                self.assertNotEqual(mat1[i,j], ret_mkl[i,j])
                self.assertEqual(ret_naive[i,j], ret_mkl[i,j])
                
    def test_zero(self):

        size = 100
        mat1, mat2, mat3, *_ = self.make_matrices(size)

        ret_naive = _matrix.multiply_naive(mat1, mat3)
        ret_mkl = _matrix.multiply_mkl(mat1, mat3)

        self.assertEqual(size, ret_naive.nrow)
        self.assertEqual(size, ret_naive.ncol)
        self.assertEqual(size, ret_mkl.nrow)
        self.assertEqual(size, ret_mkl.ncol)

        for i in range(ret_naive.nrow):
            for j in range(ret_naive.ncol):
                self.assertEqual(0, ret_naive[i,j])
                self.assertEqual(0, ret_mkl[i,j])

    def check_tile(self, mat1, mat2, tsize):

        if 0 == tsize:
            ret_tile = _matrix.multiply_naive(mat1, mat2)
            tile_str = "_matrix.multiply_naive(mat1, mat2)"
        else:
            ret_tile = _matrix.multiply_tile(mat1, mat2, tsize)
            tile_str = "_matrix.multiply_tile(mat1, mat2, tsize)"
        ret_mkl = _matrix.multiply_mkl(mat1, mat2)

        for i in range(ret_tile.nrow):
            for j in range(ret_tile.ncol):
                self.assertNotEqual(mat1[i,j], ret_mkl[i,j])
                self.assertEqual(ret_tile[i,j], ret_mkl[i,j])


        ns = dict(_matrix=_matrix, mat1=mat1, mat2=mat2, tsize=tsize)
        t_tile = timeit.Timer(tile_str, globals=ns)
        t_mkl = timeit.Timer('_matrix.multiply_mkl(mat1, mat2)', globals=ns)

        time_tile = min(t_tile.repeat(10, 1))
        time_mkl = min(t_mkl.repeat(10, 1))
        ratio = time_tile/time_mkl

        return ratio, time_tile

    def test_tile(self):

        show_ratio = bool(os.environ.get('SHOW_RATIO', False))

        mat1, mat2, *_ = self.make_matrices(500)
        
        ratio0, time0 = self.check_tile(mat1, mat2, 0)
        if show_ratio:
            print("naive ratio:", ratio0)

        ratio16, time16 = self.check_tile(mat1, mat2, 16)
        if show_ratio:
            print("tile 16 ratio:", ratio16)
            print("time16/time0:", time16/time0)
        self.assertLess(ratio16/ratio0, 0.8)

        ratio17, time17 = self.check_tile(mat1, mat2, 17)
        if show_ratio:
            print("tile 17 ratio:", ratio17)
            print("time17/time0:", time17/time0)
        self.assertLess(ratio17/ratio0, 0.8)

        ratio19, time19 = self.check_tile(mat1, mat2, 19)
        if show_ratio:
            print("tile 19 ratio:", ratio19)
            print("time19/time0:", time19/time0)
        self.assertLess(ratio19/ratio0, 0.8)