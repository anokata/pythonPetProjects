import unittest
import inventory

class TestInventory(unittest.TestCase):
    def setUp(self):
        self.inv = inventory.Inventory()

    def test_inventory_selection(self):
        self.inv.next()
        self.assertEqual(self.inv.current_cell, 1)
        self.inv.next()
        self.assertEqual(self.inv.current_cell, 2)


if __name__=='__main__':
    unittest.main()
