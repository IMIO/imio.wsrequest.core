# encoding: utf-8

from imio.wsrequest.core.base import WebserviceRequest


class Request(WebserviceRequest):

    def __init__(self, client_id, application_id, request_type, **params):
        self.client_id = client_id
        self.application_id = application_id
        self.request_type = request_type
        self.params = params
        self.files = []

    def get_result(self, response):
        return response.get('request_id')

    @property
    def query_dict(self):
        return {'client_id': self.client_id,
                'application_id': self.application_id,
                'request_type': self.request_type,
                'request_parameters': self.params,
                'files': self.files}
