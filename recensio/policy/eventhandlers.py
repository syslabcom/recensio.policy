from plone import api
from plone.app.async.interfaces import IAsyncService
from recensio.contenttypes.config import REVIEW_TYPES
from recensio.policy.export import register_doi_requestless
from zope.component import getUtility


def review_published_eventhandler(obj, evt):
    if not evt.transition or evt.transition.getId() != 'publish':
        return
    if obj.portal_type not in REVIEW_TYPES:
        return
    if not obj.isDoiRegistrationActive():
        return
    portal = api.portal.get()
    async = getUtility(IAsyncService)
    async.queueJob(register_doi_requestless, obj, portal.absolute_url())
