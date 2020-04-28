import base64
import sys

import patches
from plone.app.async.interfaces import IJobFailure
from plone.app.async.interfaces import IJobSuccess
from zc.testbrowser.browser import Browser
from zope.component import provideHandler
from zope.component.hooks import getSite
from zope.i18nmessageid import MessageFactory

recensioMessageFactory = MessageFactory("recensio")

# Subscribing to all successes/Failures of async


def successHandler(event):
    site = getSite()
    #    results = getattr(site, 'async_results', [])
    #    results.append(event.object)
    print "Success!!! %s " % event.object


def failureHandler(event):
    site = getSite()
    #    results = getattr(site, 'async_results', [])
    exc = event.object
    #    results.append("%s: %s" % (exc.type, exc.value))
    print "Failure!!!: %s" % exc


provideHandler(successHandler, [IJobSuccess])
provideHandler(failureHandler, [IJobFailure])


def viewPage(br):
    file("/tmp/bla.html", "w").write(br.contents)


def initialize(context):
    """Initializer called when used as a Zope 2 product."""
    from AccessControl import ModuleSecurityInfo
    from AccessControl import allow_module, allow_class

    allow_module("recensio.policy.utility")
    ModuleSecurityInfo("recensio.policy.utility").declarePublic("getMemberInfo")


def reloadProfiles(br, host, additional_profiles=[]):
    profiles = (
        ["profile-recensio.policy:default"]
        + additional_profiles
        + ["profile-recensio.policy:default"]
    )
    for profile in profiles:
        print "Trying to load profile %s" % profile
        br.open(host + "/portal_setup/manage_importSteps")
        br.getControl(name="context_id", index=0).value = [profile]
        br.getForm("profileform").submit()
        br.getControl("Import all steps").click()
        print "Profile %s loaded" % profile


def resetCatalog(br, host):
    print "Trying to reindex catalog"
    br.open(host + "/portal_catalog/manage_catalogAdvanced")
    br.getControl("Clear and Rebuild").click()
    assert "Catalog Rebuilt" in br.contents
    print "Catalog reindexed"
    print "Trying to clear solr"
    br.open(host + "/@@solr-maintenance/clear")
    assert "solr index cleared." in br.contents
    print "Trying to reindex solr"
    br.open(host + "/@@solr-maintenance/reindex")
    assert "solr index rebuilt." in br.contents
    print "All solr tasks done"


def reset():
    try:
        host = sys.argv[1]
        user = sys.argv[2]
        passwd = sys.argv[3]
        additional_profiles = sys.argv[4:]
    except:
        pass
    br = Browser()
    br.mech_browser.set_handle_robots(False)
    br.open(sys.argv[1])
    base64string = base64.encodestring("%s:%s" % (user, passwd))[:-1]
    br.addHeader("Authorization", "Basic %s" % base64string)
    br.reload()
    reloadProfiles(br, host, additional_profiles)
    resetCatalog(br, host)


def createSite():
    profile = ["recensio.policy:default"]
    try:
        host = sys.argv[1]
        user = sys.argv[2]
        passwd = sys.argv[3]
        profile = [sys.argv[4]]
    except:
        pass
    base64string = base64.encodestring("%s:%s" % (user, passwd))[:-1]
    br = Browser(sys.argv[1])
    print "Trying to create new plone site"
    br.addHeader("Authorization", "Basic %s" % base64string)
    br.getControl("Create a new Plone site").click()
    br.getControl(name="site_id").value = "recensio"
    br.getControl(name="extension_ids:list", index=2).value = profile
    br.getControl("Create Plone Site").click()
    print "Plone site created"
