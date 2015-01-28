# encoding: utf-8

from Products.Five.browser import BrowserView
import json

from imio.wsrequest.core.exception import RequestException
from imio.wsrequest.core.request import Request
from imio.wsrequest.core.response import Response


class WSBaseView(BrowserView):

    _render_values = {
        'success': False,
        'error': None,
    }
    render_extra_values = {}
    request_keys = ()
    request_kwargs = {}

    def render(self):
        self.request.response.setHeader('Content-Type', 'application/json')
        return json.dumps(self.render_values)

    @property
    def request_args(self):
        return [getattr(self, k) for k in self.request_keys]

    @property
    def render_values(self):
        params_list = self._render_values.keys() + self.render_extra_values.keys()
        return {k: getattr(self, k) for k in params_list}

    def _set_default_values(self, obj):
        values = self._render_values.items()
        values.extend(self.render_extra_values.items())
        for k, v in values:
            setattr(self, k, v)
        obj.webservice = self.webservice
        obj.version = self.version

    def __call__(self):
        self.ws_request = self.cls(*self.request_args,
                                   **self.request_kwargs)
        self._set_default_values(self.ws_request)
        self.execute()
        return self.render()


class WSRequestBaseView(WSBaseView):

    webservice = 'test_request'
    version = 0.1
    cls = Request

    request_keys = (
        'plone_id',
        'application_id',
        'request_type',
    )

    @property
    def request_kwargs(self):
        raise NotImplementedError

    def execute(self):
        try:
            self.success, self.id = self.ws_request.do_request()
        except RequestException, e:
            self.error = e.message


class WSResponseBaseView(WSBaseView):

    webservice = 'test_response'
    version = 0.1
    cls = Response

    request_keys = (
        'id',
    )

    @property
    def id(self):
        return self.request.get('id')

    def execute(self):
        try:
            self.success, response = self.ws_request.do_request()
            self.url = response.get('url', None)
            if response.get('external_uid'):
                self.context.external_uid = response.get('external_uid')
        except RequestException, e:
            self.error = e.message
