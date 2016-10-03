import unittest
import xoxo

class Test(unittest.TestCase):
  def test_xoxowin(self):
    gs = xoxo.GameState()
    gs.step(0,0) # X
    gs.step(4,0) # O
    gs.step(1,1)
    self.assertFalse(gs.w);
    gs.step(4,1)
    gs.step(2,2)
    self.assertTrue(gs.w);
    
    gs = xoxo.GameState()

if __name__ == '__main__':
  unittest.main()

