# encoding: utf-8

from App.config import getConfiguration
from requests.auth import HTTPBasicAuth
import requests
import json

from imio.wsrequest.core.exception import RequestException


class WebserviceRequest(object):
    version = 0.0
    webservice = 'ws'

    def do_request(self):
        """Make the request and return the uid for that request"""
        headers = {'Content-Type': 'application/json'}
        response = requests.post(
            self.url,
            auth=self.http_auth,
            data=json.dumps(self.query_dict),
            headers=headers,
        )
        if response.status_code != 200:
            raise RequestException('HTTP Error: %s' % response.status_code)
        response = response.json()
        if response.get('success') == False:
            raise RequestException('WS Error: %s' % response.get('message'))
        return self.get_result(response)

    def get_result(self, response):
        raise NotImplementedError

    @property
    def query_dict(self):
        raise NotImplementedError

    @property
    def url(self):
        return '%s/%s/%s' % (self.config.get('ws_url'),
                             self.webservice,
                             self.version)

    @property
    def http_auth(self):
        return HTTPBasicAuth(self.config.get('ws_login'),
                             self.config.get('ws_password'))

    @property
    def config(self):
        config = getattr(getConfiguration(), 'product_config', {})
        package_config = config.get('imio.wsrequest.core')
        if package_config is None:
            raise ValueError('The config for the package is missing')
        return package_config
