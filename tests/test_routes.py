import unittest

import requests

localhost = "http://127.0.0.1:5000"


# Tests to be run when flask server is running
class MyTestCase(unittest.TestCase):
    def test_1(self):
        response = requests.get(localhost + "/")
        self.equal = self.assertEqual(response.status_code, 200)

    def test_2(self):
        response = requests.get(localhost + "/ticket/1")
        self.equal = self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
