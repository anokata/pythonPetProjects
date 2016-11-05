import unittest

def gcd(a, b):
    a, b = max(a, b), min(a, b)
    while(b!=0):
        r = a % b
        a = b
        b = r
    return a

class TestGcd(unittest.TestCase):
    def test(self):
        self.assertEqual(gcd(2, 4), 2)
        self.assertEqual(gcd(2, 5), 1)
        self.assertEqual(gcd(20, 50), 10)
        self.assertEqual(gcd(50, 20), 10)

if __name__=='__main__':
    unittest.main()
