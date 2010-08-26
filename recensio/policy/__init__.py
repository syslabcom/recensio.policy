import sys
from zc.testbrowser.browser import Browser
from zope.i18nmessageid import MessageFactory
import patches

try:
    host = sys.argv[1]
    user = sys.argv[2]
    passwd = sys.argv[3]
    additional_profiles = sys.argv[4:]
except:
    pass

recensioMessageFactory = MessageFactory('recensio')

def viewPage(br):
    file('/tmp/bla.html', 'w').write(br.contents)

def initialize(context):
    """Initializer called when used as a Zope 2 product."""

def reloadProfiles(br):
    profiles = ['profile-recensio.policy:default'] + ['profile-recensio.policy:%s' % x for x in additional_profiles]
    for profile in profiles:
        br.open(host + '/portal_setup/manage_importSteps')
        br.getControl(name='context_id', index=0).value = ['profile-esc.policy:default']
        br.getForm('profileform').submit()
        br.getControl('Import all steps').click()

def resetCatalog(br):
    br.open(host + '/portal_catalog/manage_catalogAdvanced')
    br.getControl('Clear and Rebuild').click()
    assert 'Catalog Rebuilt' in br.contents

def reset():
    import pdb;pdb.set_trace()
    br = Browser(sys.argv[1])
    br.getLink('Log in').click()
    br.getControl(name='__ac_name').value = user
    br.getControl(name='__ac_password').value = passwd
    br.getControl('Log in').click()
    reloadProfiles(br)
    resetCatalog(br)

def createSite():
    import base64
    base64string = base64.encodestring('%s:%s' % (user, passwd))[:-1]
    br = Browser(sys.argv[1])
    br.addHeader('Authorization', 'Basic %s' % base64string)
    br.getControl('Create a new Plone site').click()
    br.getControl(name = 'site_id').value = 'recensio'
    br.getControl(name = 'extension_ids:list', index=2).value = ['recensio.policy:default']
    br.getControl('Create Plone Site').click()

