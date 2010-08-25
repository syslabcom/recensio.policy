from zope.i18nmessageid import MessageFactory
import patches

recensioMessageFactory = MessageFactory('recensio')

def initialize(context):
    """Initializer called when used as a Zope 2 product."""
