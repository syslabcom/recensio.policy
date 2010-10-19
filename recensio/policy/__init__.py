import base64
import sys
from zc.testbrowser.browser import Browser
from zope.i18nmessageid import MessageFactory
import patches

recensioMessageFactory = MessageFactory('recensio')

def viewPage(br):
    file('/tmp/bla.html', 'w').write(br.contents)

def initialize(context):
    """Initializer called when used as a Zope 2 product."""

def reloadProfiles(br, host, additional_profiles = []):
    profiles = ['profile-recensio.policy:default'] + additional_profiles +\
               ['profile-recensio.policy:default']
    for profile in profiles:
        print "Trying to load profile %s" % profile
        br.open(host + '/portal_setup/manage_importSteps')
        br.getControl(name='context_id', index=0).value = [profile]
        br.getForm('profileform').submit()
        br.getControl('Import all steps').click()
        print "Profile %s loaded" % profile

def resetCatalog(br, host):
    print "Trying to reindex catalog"
    br.open(host + '/portal_catalog/manage_catalogAdvanced')
    br.getControl('Clear and Rebuild').click()
    assert 'Catalog Rebuilt' in br.contents
    print "Catalog reindexed"
    print "Trying to clear solr"
    br.open(host + '/@@solr-maintenance/clear')
    assert 'solr index cleared.' in br.contents
    print "Trying to reindex solr"
    br.open(host + '/@@solr-maintenance/reindex')
    assert 'solr index rebuilt.' in br.contents
    print "All solr tasks done"

def reset():
    try:
        host = sys.argv[1]
        user = sys.argv[2]
        passwd = sys.argv[3]
        additional_profiles = sys.argv[4:]
    except:
        pass
    br = Browser(sys.argv[1])
    br.mech_browser.set_handle_robots(False)
    base64string = base64.encodestring('%s:%s' % (user, passwd))[:-1]
    br.addHeader('Authorization', 'Basic %s' % base64string)
    br.reload()
    reloadProfiles(br, host, additional_profiles)
    resetCatalog(br, host)

def createSite():
    profile = ['recensio.policy:default']
    try:
        host = sys.argv[1]
        user = sys.argv[2]
        passwd = sys.argv[3]
        profile = [sys.argv[4]]
    except:
        pass
    base64string = base64.encodestring('%s:%s' % (user, passwd))[:-1]
    br = Browser(sys.argv[1])
    print "Trying to create new plone site"
    br.addHeader('Authorization', 'Basic %s' % base64string)
    br.getControl('Create a new Plone site').click()
    br.getControl(name = 'site_id').value = 'recensio'
    br.getControl(name = 'extension_ids:list', index=2).value = profile
    br.getControl('Create Plone Site').click()
    print "Plone site created"

