import logging
import transaction

from zope import component

from Products.CMFCore.utils import getToolByName
from collective.xdv.interfaces import ITransformSettings
from plone.registry.interfaces import IRegistry


log = logging.getLogger('recensio.profile/setuphandlers.py')

def setupXDVTheme(context):
    """ Activate and configure collective.xdv
    """
    if context.readDataFile("recensio.txt") is None:
        return

    site = context.getSite()
    settings = component.getUtility(IRegistry).forInterface(ITransformSettings)
    settings.enabled = True
    settings.domains = set([u'localhost:8010', u'recensio.net'])
    settings.theme = u'python://ictextranet.theme/skins/ictextranet_theme/theme.html'
    settings.rules = u'python://ictextranet.theme/skins/ictextranet_theme/rules/default.xml'
    settings.boilerplate = u'parts/omelette/ictextranet/theme/skins/ictextranet_theme/theme.xsl'
    settings.absolute_prefix = unicode(site.getId())
    default_notheme = [
        u'^.*/emptypage$',
        u'^.*/manage$',
        u'^.*/manage_(?!translations_form)[^/]+$',
        u'^.*/image_view_fullscreen$',
        u'^.*/refbrowser_popup(\?.*)?$',
        u'^.*/error_log(/.*)?$',
        u'^.*/aq_parent(/.*)?$',
        u'^.*/portal_javascripts/.*/jscripts/tiny_mce/.*$',
        u'^.*/tinymce-upload$',
        u'^.*/.+/plone(image|link)\.htm$',
        u'^.*/plugins/table/(table|row|cell|merge_cells)\.htm$',
        u'^.*/plugins/searchreplace/searchreplace.htm$',
        u'^.*/.+/advanced/(source_editor|anchor)\.htm$',
        u'^.*/@@babblechat.*$',       # Don't interfere with Babble
        u'^.*/@@render_chat_box',     # Don't interfere with Babble
        u'^.*/manage_addProduct/.*$', # Necesary for ZMI access.
        u'^.*@@pageviewer$',          # Don't theme Pageviewer for Fancybox
        ]

    if settings.notheme != None:
        settings.notheme = set(default_notheme)
    else:
        for i in default_notheme:
            # Add / re-add any which are missing from the default
            # configuration, this won't remove additional entries
            # which may have been added manually
            settings.notheme = settings.notheme.add(i)
