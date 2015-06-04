# -*- coding: utf-8 -*-

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase
from plone.memoize.view import memoize
from plone.registry.interfaces import IRegistry
from zope.annotation import IAnnotations
from zope.component import queryUtility

from imio.wsrequest.core.browser.interfaces import IWSSettings


class WSViewlet(ViewletBase):
    annotation_key = None

    def can_view(self):
        raise NotImplementedError

    @property
    def annotation(self):
        values = IAnnotations(self.context)
        return values.get(self.annotation_key, {})

    @property
    def uid(self):
        if hasattr(self.context, 'UID'):
            return self.context.UID()
        return 0

    @property
    def registry(self):
        return queryUtility(IRegistry)


class WSConfigViewlet(WSViewlet):
    annotation_key = 'WS_CONFIG'
    index = ViewPageTemplateFile('templates/config-viewlet.pt')
    ws_request_view = '@@ws_request_config'
    ws_response_view = '@@ws_response_config'

    def can_view(self):
        return IWSSettings.providedBy(self._parent)

    @property
    def form_schema(self):
        return self._parent.form.schema

    @property
    @memoize
    def registry_config(self):
        return self.registry.forInterface(self._parent.form.schema,
                                          check=False)

    def can_sync(self):
        """
        Ensure that the required field in control panel config are defined
        """
        mandatory_fields = ('client_id', 'application_id', 'type_version')
        for fieldname in mandatory_fields:
            if not getattr(self.registry_config, fieldname):
                return False
        return True

    @property
    def last_sync_date(self):
        date = self.annotation.get('last_sync_date')
        return date and date.strftime('%d/%m/%Y %H:%M') or ''

    @property
    def request_id(self):
        return self.annotation.get('id', '')

    @property
    def ws_request_url(self):
        return '%s/%s' % (self.context.absolute_url(), self.ws_request_view)

    @property
    def ws_response_url(self):
        return '%s/%s' % (self.context.absolute_url(), self.ws_response_view)
