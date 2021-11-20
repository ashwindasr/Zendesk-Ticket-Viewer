import unittest

import requests

localhost = "http://127.0.0.1:5000"


class MyTestCase(unittest.TestCase):
    def test_1(self):
        response = requests.get(localhost + "/posts")
        self.equal = self.assertEqual(response.status_code, 200)

    def test_2(self):
        response = requests.get(localhost + "/posts/show/1")
        self.equal = self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
