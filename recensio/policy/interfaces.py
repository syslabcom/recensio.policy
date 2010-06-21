from Products.ATContentTypes.interfaces.topic import IATTopic
from zope.interface import Interface
from zope import schema
from recensio.policy import recensioMessageFactory as _

class IDiscussionCollections(IATTopic):
    pass


class IWorkflowHelper(Interface):
    
    def handleTransition(wf_variable):
        """ Action that is performed after a workflow change, e.g.
            send a notification e-mail.
        """

class IRecensioSettings(Interface):
    """ Global recensio settings. This describes records stored in the
    configuration registry and obtainable via plone.registry.
    """

    review_submitted_email = schema.TextLine(
        title=_(u'label_review_submitted_email', default=u'E-mail '
            'address for submitted reviews.'),
        description=_(u'description_review_submitted_email', default=u'Enter '
            'an e-mail address to which notifications will be sent, if a user '
            'submits a review for publication.'),
        required=False,
        default=u'',
        )
