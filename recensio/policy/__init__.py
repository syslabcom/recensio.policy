from zc.testbrowser.browser import Browser
from zope.i18nmessageid import MessageFactory
import patches
import sys

host = sys.argv[1]
user = sys.argv[2]
passwd = sys.argv[3]
additional_profiles = sys.argv[4:]

recensioMessageFactory = MessageFactory('recensio')

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
    br = Browser(sys.argv[1])
    br.getLink('Log in').click()
    br.getControl(name='__ac_name').value = user
    br.getControl(name='__ac_password').value = passwd
    br.getControl('Log in').click()
    reloadProfiles(br)
    resetCatalog(br)

