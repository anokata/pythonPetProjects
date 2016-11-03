import unittest
from sorting import *
import euler40

class TestSort(unittest.TestCase):
    def test_sort(self):
        self.assertEqual(sort([1,2,3]), [1,2,3])
        a = [1,2,3]
        b = sort(a)
        a[1] = 10
        self.assertNotEqual(a,b)
        #self.assertEqual(sort[3,2,1], [1,2,3])

class TestE40(unittest.TestCase):
    def test_gen(self):
        self.assertEqual(euler40.gen_cham_const(15), '123456789101112131415')

if __name__=='__main__':
    unittest.main()

