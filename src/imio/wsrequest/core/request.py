# encoding: utf-8

from App.config import getConfiguration
from requests.auth import HTTPBasicAuth
import requests
import json

from imio.wsrequest.core.exception import RequestException


class Request(object):
    version = '0.0'

    def __init__(self, client_id, application_id, request_type, **params):
        self.client_id = client_id
        self.application_id = application_id
        self.request_type = request_type
        self.params = params

    def do_request(self):
        """Make the request and return the uid for that request"""
        headers = {'Content-Type': 'application/json'}
        response = requests.post(
            self.url,
            auth=self.http_auth,
            data=self.json_query,
            headers=headers,
        )
        if response.status_code != 200:
            raise RequestException('HTTP Error: %s' % response.status_code)
        response = response.json()
        if response.get('success') == False:
            raise RequestException('WS Error: %s' % response.get('message'))
        return response.get('request_id')

    @property
    def url(self):
        return '%s/test_request/%s' % (self.config.get('ws_url'), self.version)

    @property
    def http_auth(self):
        return HTTPBasicAuth(self.config.get('ws_login'),
                             self.config.get('ws_password'))

    @property
    def json_query(self):
        return json.dumps({'client_id': self.client_id,
                           'application_id': self.application_id,
                           'request_type': self.request_type,
                           'request_parameters': self.params})

    @property
    def config(self):
        config = getattr(getConfiguration(), 'product_config', {})
        package_config = config.get('imio.wsrequest.core')
        if package_config is None:
            raise ValueError('The config for the package is missing')
        return package_config
