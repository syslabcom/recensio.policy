# -*- coding: utf-8 -*-


from zope.interface import implements
from zope import schema
from plone.app.users.userdataschema import IUserDataSchemaProvider, IUserDataSchema
from collective.captcha.form import Captcha
from zope.i18nmessageid import MessageFactory
_ = MessageFactory("recensio")

UNWANTED_FIELDS_FOR_PERSONAL_PREFERENCES = (
    'declaration_of_identity',
    'captcha',
    'portrait',
    'pdelete',
    )


class UserDataSchemaProvider(object):
    implements(IUserDataSchemaProvider)

    def getSchema(self):
        """
        """
        return IRecensioUserDataSchema

def validateAccept(value):
    if not value == True:
        return False
    return True


class IRecensioUserDataSchema(IUserDataSchema):
    """ Use all the fields from the default user data schema, and add various
    extra fields.
    """
    academic_title = schema.TextLine(
        title=_(u'label_academic_title', default=u'Academic title'),
        description=_(u'help_academic_title',
                      default=u"Please add your academic titles here"),
        required=False,
        )

    firstname = schema.TextLine(
        title=_(u'label_firstname', default=u'First name'),
        required=True,
        )

    lastname = schema.TextLine(
        title=_(u'label_lastname', default=u'Last name'),
        required=True,
        )

    # Note: the available languages should come from a vocabulary!
    preferred_language = schema.Choice(
        title=_(u'label_preferred_language', default=u'Preferred language'),
        description=_(u'description_preferred_language', default=u'What '
            'language do you prefer for receiving e-mails from us?'),
        required=True,
        vocabulary="recensio.policy.vocabularies.available_user_languages",
        # values = [u'English', u'Deutsch', u'Francais'],
        )

    declaration_of_identity = schema.Bool(
        title=_(u'label_declaration_of_identity', default=u'Declaration of identity'),
        description=_(u'help_declaration_of_identity',
                      default=u"I declare that I am indeed the person "
                      "identified by the entries above. "),
        required=True,
        constraint=validateAccept,
        )

    captcha = Captcha(
        title=_(u'Type the code'),
        description=_(u'Type the code from the picture shown below or '
                   u'from the audio.'),
        )

