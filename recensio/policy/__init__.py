import base64
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
    profiles = ['profile-recensio.policy:default'] + additional_profiles
    for profile in profiles:
        br.open(host + '/portal_setup/manage_importSteps')
        br.getControl(name='context_id', index=0).value = [profile]
        br.getForm('profileform').submit()
        br.getControl('Import all steps').click()

def resetCatalog(br):
    br.open(host + '/portal_catalog/manage_catalogAdvanced')
    br.getControl('Clear and Rebuild').click()
    assert 'Catalog Rebuilt' in br.contents

def reset():
    br = Browser(sys.argv[1])
    base64string = base64.encodestring('%s:%s' % (user, passwd))[:-1]
    br.addHeader('Authorization', 'Basic %s' % base64string)
    br.reload()
    reloadProfiles(br)
    resetCatalog(br)

def createSite():
    base64string = base64.encodestring('%s:%s' % (user, passwd))[:-1]
    br = Browser(sys.argv[1])
    br.addHeader('Authorization', 'Basic %s' % base64string)
    br.getControl('Create a new Plone site').click()
    br.getControl(name = 'site_id').value = 'recensio'
    br.getControl(name = 'extension_ids:list', index=2).value = ['recensio.policy:default']
    br.getControl('Create Plone Site').click()

