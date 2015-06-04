# -*- coding: utf-8 -*-

from datetime import datetime
from plone.memoize.view import memoize
from plone.registry.interfaces import IRegistry
from zope.annotation import IAnnotations
from zope.component import getMultiAdapter
from zope.component import queryUtility

from imio.wsrequest.core import WSRequestBaseView
from imio.wsrequest.core import WSResponseBaseView


class WSRequestConfigView(WSRequestBaseView):
    annotation_key = 'WS_CONFIG'
    request_type = 'CONFIG'
    json_extra_values = {
        'id': None,
    }

    @property
    def referer(self):
        view_name = self.request.get('HTTP_REFERER').split('/')[-1]
        view_name = view_name.replace('@@', '', 1)
        return getMultiAdapter((self.context, self.request), name=view_name)

    @property
    @memoize
    def registry_config(self):
        registry = queryUtility(IRegistry)
        return registry.forInterface(self.referer.form.schema, check=False)

    @property
    def client_id(self):
        return self.registry_config.client_id

    @property
    def application_id(self):
        return self.registry_config.application_id

    @property
    def type_version(self):
        return self.registry_config.type_version

    @property
    def request_kwargs(self):
        return {}

    def store_values(self):
        values = {'id': self.id}
        set_annotation(self.context, self.annotation_key, values, update=True)


class WSResponseConfigView(WSResponseBaseView):
    annotation_key = 'WS_CONFIG'
    json_extra_values = {
        'response': None,
    }

    def store_values(self):
        values = {'config': self.response.get('config'),
                  'date': datetime.now()}
        set_annotation(self.context, self.annotation_key, values)


def set_annotation(context, key, values, update=False):
    annotations = IAnnotations(context)
    if key not in annotations:
        annotations[key] = {}
    if update is True:
        annotations[key].update(values)
    else:
        annotations[key] = values
