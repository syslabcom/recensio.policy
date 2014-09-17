from Products.Five.browser import BrowserView
from zope.app.pagetemplate import ViewPageTemplateFile
from datetime import datetime
from plone.uuid.interfaces import IUUID
from os import path
from Products.CMFCore.utils import getToolByName
from recensio.contenttypes.interfaces.review import IParentGetter
from plone.i18n.locales.languages import _languagelist

from recensio.policy.constants import \
    EXPORTABLE_CONTENT_TYPES, EXPORT_OUTPUT_PATH, EXPORT_MAX_ITEMS

AUTHOR_TMPL = """        <author_%(num)s_first_name>%(firstname)s</author_%(num)s_first_name>
        <author_%(num)s_last_name>%(lastname)s</author_%(num)s_last_name>
"""
EDITOR_TMPL = """        <editor_%(num)s_first_name>%(firstname)s</editor_%(num)s_first_name>
        <editor_%(num)s_last_name>%(lastname)s</editor_%(num)s_last_name>
"""


class Book(object):

    def __init__(self, obj):
        issn = getattr(obj, 'getIssn', lambda: None)
        self.isbn = getattr(obj, 'getIsbn', issn)()
        self.subtitle = obj.title
        self.title = obj.getSubtitle()
        self.year = obj.getYearOfPublication()
        self.author_1 = {'first_name': '', 'last_name': obj.getReviewAuthor()}
        self.author_2 = {'first_name': '', 'last_name': ''}
        self.author_3 = {'first_name': '', 'last_name': ''}

    @property
    def author(self):
        retval = None
        for i in range(1):  # We don't support multiple authors
            try:
                retval[i]['first_name'] = ''
                retval[i]['last_name'] = self.obj.getAuthors()
            except IndexError:
                pass
        return retval


class Review(object):
    def __init__(self, catalog_entry):
        self.obj = catalog_entry.getObject()
        self.id = catalog_entry.getPath()
        self.filename = catalog_entry.getURL()

    @property
    def reviewers(self):
        for i in [range(1)]:  # No multiple authors support in our system
            yield {'last_name': self.obj.getAuthors(),
                   'first_name': ''}

    @property
    def books(self):
        return [Book(self.obj) for x in [range(1)]]  # No multiple books
                                                     # support in our system


class DigiToolRepresentation(BrowserView):
    """ if this view is called, it iterates through the system and dumps every
    content type as xml to harddisk and marks it as exported with a little
    flag. If the flag is set, it is not exported again. """

    template = ViewPageTemplateFile('templates/digitool.pt')

    def __call__(self):
        return self.template(self)


class XMLRepresentation(BrowserView):
    template = None
    filename = "recensio_exportx.xml"

    def get_lang_name(self, code):
        return _languagelist.get(code, {'native': code})['native']

    def get_parent(self, meta_type):
        return IParentGetter(self.context).get_parent_object_of_type(meta_type)

    def get_voc_title(self, typ, term):
        voc = getToolByName(self.context, 'portal_vocabularies', None)

        self.vocDict = dict()
        self.vocDict['ddcPlace'] = voc.getVocabularyByName(
            'region_values')
        self.vocDict['ddcTime'] = voc.getVocabularyByName(
            'epoch_values')
        self.vocDict['ddcSubject'] = voc.getVocabularyByName(
            'topic_values')

        term = self.vocDict[typ].getTermByKey(term)
        if not term:
            return ''
        return term

    def list_authors(self):
        out = ""
        num = 1
        for author in self.context.getAuthors():
            out += AUTHOR_TMPL % dict(
                num=num,
                firstname=author['firstname'],
                lastname=author['lastname'])
            num += 1
        return out

    def list_editors(self):
        out = ""
        num = 1
        for editor in self.context.getEditorial():
            out += EDITOR_TMPL % dict(
                num=num,
                firstname=editor['firstname'],
                lastname=editor['lastname'])
            num += 1
        return out


class XMLRepresentation_rj(XMLRepresentation):
    template = ViewPageTemplateFile('templates/export_rj.pt')

    def __call__(self):
        return self.template(self)


class XMLRepresentation_rm(XMLRepresentation):
    template = ViewPageTemplateFile('templates/export_rm.pt')

    def __call__(self):
        return self.template(self)


class XMLRepresentation_publication(XMLRepresentation):
    template = ViewPageTemplateFile('templates/export_container.pt')

    def __call__(self):
        self.request.response.setHeader(
            'Content-type',
            'application/xml')
        self.request.response.setHeader(
            'Content-disposition',
            'inline;filename=%s' % self.filename())
        return self.template(self)

    def filename(self):
        return "recensio_%s_%s_%s.xml" % (
            self.get_publication_shortname(), "0", "0")

    def reviews(self):
        pc = self.context.portal_catalog
        parent_path = dict(query='/'.join(self.context.getPhysicalPath()),
                           depth=3)
        results = pc(review_state="published",
                     portal_type=("Review Monograph", "Review Journal"),
                     path=parent_path)
        for item in results:
            yield item.getObject()

    def get_publication_shortname(self):
        return unicode(self.get_parent("Publication").getId(), 'utf-8')

    def get_package_journal_pubyear(self):
        return None
        #return self.get_parent("Publication")

    def get_package_journal_name(self):
        return unicode(self.get_parent("Publication").Title(), 'utf-8')

    def get_package_journal_volume(self):
        return u"Not Available"

    def get_package_journal_issue(self):
        return None


class XMLRepresentation_volume(XMLRepresentation_publication):
    template = ViewPageTemplateFile('templates/export_container.pt')

    def get_package_journal_volume(self):
        return unicode(self.get_parent("Volume").Title(), 'utf-8')

    def get_package_journal_issue(self):
        return None

    def filename(self):
        return "recensio_%s_%s_%s.xml" % (
            self.get_publication_shortname(),
            self.get_package_journal_volume(),
            "0")


class XMLRepresentation_issue(XMLRepresentation_volume):
    template = ViewPageTemplateFile('templates/export_container.pt')

    def get_package_journal_issue(self):
        return unicode(self.get_parent("Issue").Title(), 'utf-8')

    def filename(self):
        return "recensio_%s_%s_%s.xml" % (
            self.get_publication_shortname(),
            self.get_package_journal_volume(),
            self.get_package_journal_issue())


class DigiToolExport(BrowserView):
    """ if this view is called, it iterates through the system and dumps every
    content type as xml to harddisk and marks it as exported with a little
    flag. If the flag is set, it is not exported again. """

    def __call__(self):
        """ run idempotent. Handle a number of records and return. """
        portal = self.context.portal_url.getPortalObject()

        now = datetime.now()
        count = 0
        for key, value in portal.ZopeFind(portal, search_sub=1):
            ob = value.aq_explicit
            if (hasattr(ob, '__digitool_exported__') or
                    not hasattr(ob, 'portal_type') or
                    ob.portal_type not in EXPORTABLE_CONTENT_TYPES):
                continue

            try:
                self.dump_xml(value)
            except KeyError, ke:
                print ke
                continue

            #setattr(value, '__digitool_exported__', True)
            count += 1
            if count > EXPORT_MAX_ITEMS:
                break

        delta = datetime.now() - now
        print "Exporting %s items takes %s secs" % (EXPORT_MAX_ITEMS, delta)
        return "ok %s" % delta

    def dump_xml(self, item):
        """ create an xml representation of the object and dump it to disk """

        data = item.unrestrictedTraverse('@@digitool-xml')
        filename = "%s/%s.xml" % (EXPORT_OUTPUT_PATH, IUUID(item))
        if path.exists(filename):
            print "File exists, overwriting"
            #raise KeyError, "File exists, but must not"

        fh = open(filename, "w")
        fh.write(data())
        fh.close()

    @property
    def reviews(self):
        return [Review(x) for x in self.context.queryCatalog()]
