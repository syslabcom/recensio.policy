# -*- coding: utf-8 -*-


from zope.interface import implements
from zope import schema
from plone.app.users.userdataschema import IUserDataSchemaProvider, IUserDataSchema
from zope.i18nmessageid import MessageFactory
_ = MessageFactory("recensio")

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
        title=_(u'label_academic_title', default=u'Titel'),
        description=_(u'help_academic_title',
                      default=u""),
        required=False,
        )

    # Note: the available languages should come from a vocabulary!
    preferred_language = schema.Choice(
        title=_(u'label_preferred_language', default=u'Bevozugte Sprache'),
        description=_(u'description_preferred_language', default=u''),
        required=True,
        values = [u'English', u'Deutsch', u'Français'],
        )

    declaration_of_identity = schema.Bool(
        title=_(u'label_declaration_of_identity', default=u'Erklärung der eigenen Identität'),
        description=_(u'help_declaration_of_identity',
                      default=u"Ich versichere, die in diesem Formular"
                      " angegebene Person zu sein. "),
        required=True,
        constraint=validateAccept,
        )
