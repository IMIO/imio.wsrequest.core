# encoding: utf-8

from imio.wsrequest.core.base import WebserviceRequest


class Response(WebserviceRequest):

    def __init__(self, request_id):
        self.request_id = request_id

    def get_result(self, response):
        return response.get('response')

    @property
    def query_dict(self):
        return {'request_id': self.request_id}
