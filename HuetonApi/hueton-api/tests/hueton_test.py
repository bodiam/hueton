import unittest
from ..hueton_api import HuetonApi

class HuetonTest(unittest.TestCase):

	def test_hello_world(self):
		print("hello")
		self.assertEquals(4, 4)

	def test_register_new_developer(self):
		api = HuetonApi()
		api.init('username')

		self.assertFalse(api.connect())

		api.register()

		self.assertTrue(api.connect())
		
	

if __name__ == '__main__':
    unittest.main()
