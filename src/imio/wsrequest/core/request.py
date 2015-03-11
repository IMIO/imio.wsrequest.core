# encoding: utf-8

from imio.wsrequest.core.base import WebserviceRequest


class Request(WebserviceRequest):

    def __init__(self,
                 client_id,
                 application_id,
                 request_type,
                 type_version,
                 **params):
        self.client_id = client_id
        self.application_id = application_id
        self.request_type = request_type
        self.type_version = type_version
        self.params = params
        self.files = []

    def get_result(self, response):
        return response.get('success'), response.get('request_id')

    @property
    def query_dict(self):
        return {'client_id': self.client_id,
                'application_id': self.application_id,
                'request_type': self.request_type,
                'type_version': self.type_version,
                'request_parameters': self.params,
                'files': self.files}
