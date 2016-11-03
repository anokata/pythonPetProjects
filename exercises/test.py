import unittest
from sorting import *

class TestSort(unittest.TestCase):
    def test_sort(self):
        self.assertEqual(sort([1,2,3]), [1,2,3])
        a = [1,2,3]
        b = sort(a)
        a[1] = 10
        self.assertNotEqual(a,b)
        self.assertEqual(sort[3,2,1], [1,2,3])

if __name__=='__main__':
    unittest.main()

