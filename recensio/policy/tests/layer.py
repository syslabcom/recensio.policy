from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting

from plone.testing import z2

from zope.configuration import xmlconfig
from zope.interface import implements

from Products.CMFCore.utils import getToolByName
from plone.app.async.interfaces import IAsyncService

_async_layer_db = None


class DummyAsync(object):
    implements(IAsyncService)

    def queueJob(self, *args, **kwargs):
        pass

    def queueJobWithDelay(self, *args, **kwargs):
        pass


class RecensioPolicyWithoutContent(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import plone.app.theming
        xmlconfig.file('configure.zcml', plone.app.theming, \
            context=configurationContext)
        import recensio.theme
        xmlconfig.file('configure.zcml', recensio.theme, \
            context=configurationContext)
        import recensio.policy
        xmlconfig.file('configure.zcml', recensio.policy, \
            context=configurationContext)
        import plone.app.intid
        xmlconfig.file('configure.zcml', plone.app.intid, \
            context=configurationContext)

        z2.installProduct(app, 'recensio.contenttypes')
        z2.installProduct(app, 'Products.PythonScripts')
        z2.installProduct(app, 'Products.LinguaPlone')
        z2.installProduct(app, 'Products.ATVocabularyManager')

    def setUpPloneSite(self, portal):
        wftool = getToolByName(portal, 'portal_workflow')
        wftool.setDefaultChain('plone_workflow')
        applyProfile(portal, 'Products.CMFPlone:plone-content')
        applyProfile(portal, 'plone.app.theming:default')
        applyProfile(portal, 'recensio.policy:default')
        applyProfile(portal, 'recensio.policy:test')

        sm = portal.getSiteManager()
        sm.registerUtility(factory=DummyAsync, provided=IAsyncService)


class RecensioPolicy(RecensioPolicyWithoutContent):

    def setUpPloneSite(self, portal):
        super(RecensioPolicy, self).setUpPloneSite(portal)
        applyProfile(portal, 'recensio.contenttypes:example_content')

RECENSIO_FIXTURE = RecensioPolicy()
RECENSIO_FIXTURE_WITHOUT_CONTENT = RecensioPolicyWithoutContent()
RECENSIO_BARE_INTEGRATION_TESTING = IntegrationTesting(bases=(RECENSIO_FIXTURE_WITHOUT_CONTENT, ),
    name="RecensioPolicy:IntegrationWithoutContent")
RECENSIO_INTEGRATION_TESTING = IntegrationTesting(bases=(RECENSIO_FIXTURE, ),
    name="RecensioPolicy:Integration")
RECENSIO_FUNCTIONAL_TESTING = FunctionalTesting(bases=(RECENSIO_FIXTURE, ),
    name="RecensioPolicy:Functional")
