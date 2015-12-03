from Testing.makerequest import makerequest
from plone import api
from recensio.policy.browser.export import MetadataExport
from zope.component.hooks import setHooks
from zope.component.hooks import setSite
import Zope2
import logging
import sys
import transaction

log = logging.getLogger(__name__)


def metadata_export(config_file, run_as):
    Zope2.Startup.run.configure(config_file)
    app = makerequest(Zope2.app())
    setHooks()
    portal = app.objectValues('Plone Site')[0]
    setSite(portal)

    log.setLevel(logging.DEBUG)
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    log.addHandler(handler)

    with api.env.adopt_user(username=run_as):
        me = MetadataExport(portal, portal.REQUEST)
        me()
    transaction.commit()
