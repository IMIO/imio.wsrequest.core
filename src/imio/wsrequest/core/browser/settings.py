# -*- coding: utf-8 -*-

from Products.statusmessages.interfaces import IStatusMessage
from collective.z3cform.datagridfield import DataGridFieldFactory
from collective.z3cform.datagridfield.registry import DictRow
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.app.registry.browser.controlpanel import RegistryEditForm
from z3c.form import button
from z3c.form import field
from zope import schema
from zope.interface import Interface
from zope.interface import implements
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.vocabulary import SimpleTerm

from imio.wsrequest.core.i18n import _
from imio.wsrequest.core.browser.interfaces import IWSSettings


def _application_id_values():
    values = {
        'PM': u'Plone Meeting',
        'DMS': u'Ged',
        'PST': u'PST',
        'URB': u'Urban',
    }

    for key, name in values.items():
        yield SimpleTerm(value=key, token=key, title=name)

application_id_vocabulary = SimpleVocabulary(list(_application_id_values()))


class IUserMappingsSchema(Interface):
    """Schema used for the datagrid field 'user_mappings'"""

    local_userid = schema.TextLine(
        title=_("Local user id"),
        required=True,
    )

    remote_userid = schema.TextLine(
        title=_("Remote user id"),
        required=True,
    )


class IWSRequestSettings(Interface):

    client_id = schema.TextLine(
        title=_(u'Remote client id'),
        required=True,
    )

    application_id = schema.Choice(
        title=_(u'Application id'),
        vocabulary=application_id_vocabulary,
        required=True,
    )

    type_version = schema.TextLine(
        title=_(u'Webservice version'),
        required=True,
        default=u'0.1',
    )

    user_mappings = schema.List(
        title=_('User ids mappings'),
        description=_("By default, while sending an element to an external "
                      "Plone, the user id of the logged in user is used and a "
                      "binding is made to the same user id in PloneMeeting. "
                      "If the local user id does not exist in PloneMeeting, "
                      "you can define here the user mappings to use. "
                      "For example : 'jdoe' in 'Local user id' of the current "
                      "application correspond to 'johndoe' in remote Plone."),
        value_type=DictRow(title=_("User mappings"),
                           schema=IUserMappingsSchema,
                           required=False),
        required=False,
    )


class WSRequestSettingsEditForm(RegistryEditForm):
    schema = IWSRequestSettings
    fields = field.Fields(IWSRequestSettings)
    fields['user_mappings'].widgetFactory = DataGridFieldFactory

    @button.buttonAndHandler(_('Save'), name=None)
    def handleSave(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        self.applyChanges(data)
        IStatusMessage(self.request).addStatusMessage(_(u"Changes saved"),
                                                      "info")

    @button.buttonAndHandler(_('Cancel'), name='cancel')
    def handleCancel(self, action):
        IStatusMessage(self.request).addStatusMessage(_(u"Edit cancelled"),
                                                      "info")
        self.request.response.redirect("%s/%s" % (self.context.absolute_url(),
                                                  self.control_panel_view))


class WSRequestSettings(ControlPanelFormWrapper):
    implements(IWSSettings)
    form = WSRequestSettingsEditForm
