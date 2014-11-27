# encoding: utf-8

from imio.wsrequest.core.request import Request
from mock import Mock
import requests
import unittest


class TestRequest(unittest.TestCase):

    def setUp(self):
        Request.config = {'ws_url': 'http://127.0.0.1:6543',
                          'ws_login': 'testuser',
                          'ws_password': 'test'}

    @property
    def fake_response(self):
        body = {'success': True, 'request_id': 100}
        response = {'status_code': 200,
                    'json': Mock(return_value=body)}
        return type('response', (object, ), response)

    def test_do_request(self):
        requests.post = Mock(return_value=self.fake_response)
        request = Request('A', '1', 'test', foo='bar', bar='foo')
        request.version = 0.1
        id = request.do_request()
        self.assertEqual(100, id)
