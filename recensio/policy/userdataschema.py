# -*- coding: utf-8 -*-


from zope.interface import implements
from zope import schema
from plone.app.users.userdataschema import IUserDataSchemaProvider, IUserDataSchema
# from quintagroup.formlib.captcha import Captcha
from zope.i18nmessageid import MessageFactory
_ = MessageFactory("recensio")

class UserDataSchemaProvider(object):
    implements(IUserDataSchemaProvider)

    def getSchema(self):
        """
        """
        return IRecensioUserDataSchema




class IRecensioUserDataSchema(IUserDataSchema):
    """ Use all the fields from the default user data schema, and add various
    extra fields.
    """
    academic_title = schema.TextLine(
        title=_(u'label_academic_title', default=u'Titel'),
        description=_(u'help_academic_title',
                      default=u""),
        required=False,
        )

    # Note: the available languages should come from a vocabulary!
    preferred_language = schema.Choice(
        title=_(u'label_preferred_language', default=u'Preferred language'),
        description=_(u'description_preferred_language', default=u''),
        required=True,
        values = [u'English', u'Deutsch', u'Francais'],
        )

    declaration_of_identity = schema.Choice(
        title=_(u'label_declaration_of_identity', default=u'Declaration of identity'),
        description=_(u'help_declaration_of_identity',
                      default=u"I declare that I am indeed the person "
                      "identified by the entries above. "),
        required=True,
        values = [u'OK'],
        )

    # captcha = Captcha(
    #     title=_(u'label_captcha', default=u'Enter the code as shown'),
    #     description=_(u'description_captcha', default=u''),
    # )