import unittest
from sell_product import sell



class Test_01(unittest.TestCase):

    sell_instance = sell()
    def test(self):
        self.assertEqual(2,self.sell_instance.file())


if __name__ == "__main__":

    unittest.main()