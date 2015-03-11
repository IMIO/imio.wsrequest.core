# encoding: utf-8

from Products.Five.browser import BrowserView
import json

from imio.wsrequest.core.exception import RequestException
from imio.wsrequest.core.request import Request
from imio.wsrequest.core.response import Response


class WSBaseView(BrowserView):
    """Base class for requests and responses queries"""

    # Mandatory values returned by the webservice
    # format : {key: default_value}
    _default_json_values = {
        'success': False,
        'error': None,
    }
    # Dictionary with extra values returned by the webservice
    # format : {key: default_value}
    json_extra_values = {}
    # List of parameters required by the webservice
    request_keys = ()
    # Dictionary of optionals parameters
    # format : {key: value}
    request_kwargs = {}

    def render(self):
        """Return a JSON with the desired values from the webservice result"""
        self.request.response.setHeader('Content-Type', 'application/json')
        return json.dumps(self._json_values)

    @property
    def request_args(self):
        """Return a list with the parameters required by the webservice"""
        return [getattr(self, k) for k in self.request_keys]

    @property
    def _json_values(self):
        """Return a dictionary with the values for JSON render"""
        keys = self._default_json_values.keys() + self.json_extra_values.keys()
        return {k: getattr(self, k) for k in keys}

    def _set_default_values(self, obj):
        """Set the default values"""
        values = self._default_json_values.items()
        values.extend(self.json_extra_values.items())
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

    def execute(self):
        """Execute the request to the webservice and return the result"""
        raise NotImplementedError


class WSRequestBaseView(WSBaseView):
    """Base class for requests queries"""

    webservice = 'test_request'
    version = 0.1
    cls = Request

    request_keys = (
        'plone_id',
        'application_id',
        'request_type',
        'type_version',
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
    """Base class for responses queries"""

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
