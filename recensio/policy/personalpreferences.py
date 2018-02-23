from zope.component import getUtility
from zope.formlib import form
from plone.app.users.browser.personalpreferences import UserDataPanel
from plone.app.users.browser.personalpreferences import UserDataConfiglet
from plone.app.users.userdataschema import IUserDataSchemaProvider
from Products.CMFDefault.formlib.widgets import FileUploadWidget
from userdataschema import UNWANTED_FIELDS_FOR_PERSONAL_PREFERENCES


class RecensioUserDataPanel(UserDataPanel):

    def __init__(self, context, request):
        """ Load the UserDataSchema at view time. 
        (Because doing getUtility for IUserDataSchemaProvider fails at startup
        time.)

        We override Plone's default, in order to filter out the unwanted fields
        for the personal preferences form.
        """
        super(RecensioUserDataPanel, self).__init__(context, request)
        util = getUtility(IUserDataSchemaProvider)
        schema = util.getSchema()
        fields = form.FormFields(schema)
        self.form_fields = fields.omit(*UNWANTED_FIELDS_FOR_PERSONAL_PREFERENCES)


class RecensioUserDataConfiglet(UserDataConfiglet, RecensioUserDataPanel):
        """ We override Plone's default, in order to filter out the unwanted fields
            for the personal preferences form.
        """
