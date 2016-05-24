from App.config import getConfiguration
from Products.CMFPlone.utils import safe_unicode
from logging import getLogger
from plone.registry.interfaces import IRegistry
from recensio.policy.interfaces import IRecensioSettings
from zope.app.publication.zopepublication import ZopePublication
from zope.component import getUtility
from zope.component.hooks import setSite
import Zope2
import transaction


configuration = getConfiguration()
if not hasattr(configuration, 'product_config'):
    conf = None
else:
    conf = configuration.product_config.get('recensio.policy')

log = getLogger('recensio.policy')

def dbconfig(event):
    if conf is None:
        log.error('No product config found! Configuration will not be set')
        return
    db = Zope2.DB
    connection = db.open()
    root_folder = connection.root().get(ZopePublication.root_name, None)
    for portal_id in conf.get('portals', '').split(','):
        portal = root_folder.get(portal_id)
        if not portal:
            log.error('No such portal: ' + portal_id)
            continue
        url = conf.get('.'.join((portal_id, 'external_url')))
        if not url:
            log.error('No external_url provided for ' + portal_id)
            continue
        setSite(portal)
        registry = getUtility(IRegistry)
        try:
            recensio_settings = registry.forInterface(IRecensioSettings)
        except Exception as e:
            log.exception(e)
            log.error('Could not get recensio settings for ' + portal_id)
            continue
        if recensio_settings.external_portal_url != safe_unicode(url):
            recensio_settings.external_portal_url = safe_unicode(url)

    transaction.commit()
