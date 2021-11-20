import unittest
from routes import get_response_json
import os
import requests


class MyTestCase(unittest.TestCase):
    def test_1(self):
        credentials = os.environ['EMAIL'], os.environ['PASSWORD']
        session = requests.Session()
        session.auth = credentials
        server = os.environ['MY_SERVER']
        zendesk = f'https://{server}.zendesk.com'
        url = f'{zendesk}/api/v2/tickets.json?page[size]=25'

        answer = get_response_json(url)
        self.assertTrue(answer['tickets'] is not None)

    def test_2(self):
        credentials2 = "a@email.com", "password"
        session2 = requests.Session()
        session2.auth = credentials2
        server2 = "server"
        zendesk2 = f'https://{server2}.zendesk.com'
        url2 = f'{zendesk2}/api/v2/tickets.json?page[size]=25'

        answer = get_response_json(url2)
        print(answer)
        self.assertTrue(answer['error']['title'] == 'No help desk at server.zendesk.com')


if __name__ == '__main__':
    unittest.main()
