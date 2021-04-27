from cgi import escape
from io import BytesIO
from plone.i18n.locales.languages import _languagelist
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from recensio.contenttypes.config import REVIEW_TYPES
from recensio.contenttypes.interfaces.review import IParentGetter
from zipfile import ZipFile
from zope.app.pagetemplate import ViewPageTemplateFile


AUTHOR_TMPL = """        <author_%(num)s_first_name>%(firstname)s</author_%(num)s_first_name>
        <author_%(num)s_last_name>%(lastname)s</author_%(num)s_last_name>
"""
EDITOR_TMPL = """        <editor_%(num)s_first_name>%(firstname)s</editor_%(num)s_first_name>
        <editor_%(num)s_last_name>%(lastname)s</editor_%(num)s_last_name>
"""


class XMLRepresentation(BrowserView):
    filename = "recensio_exportx.xml"
    include_fulltext = False

    def get_lang_name(self, code):
        return _languagelist.get(code, {"native": code})["native"]

    def get_parent(self, meta_type):
        return IParentGetter(self.context).get_parent_object_of_type(meta_type)

    def get_publication_shortname(self):
        return unicode(self.get_parent("Publication").getId(), "utf-8")

    def get_publication_title(self):
        return unicode(self.get_parent("Publication").Title(), "utf-8")

    def get_package_journal_volume(self):
        return unicode(self.get_parent("Volume").getId(), "utf-8")

    def get_package_journal_volume_title(self):
        return unicode(self.get_parent("Volume").Title(), "utf-8")

    def get_voc_title(self, typ, term):
        voc = getToolByName(self.context, "portal_vocabularies", None)

        self.vocDict = dict()
        self.vocDict["ddcPlace"] = voc.getVocabularyByName("region_values")
        self.vocDict["ddcTime"] = voc.getVocabularyByName("epoch_values")
        self.vocDict["ddcSubject"] = voc.getVocabularyByName("topic_values")

        term = self.vocDict[typ].getTermByKey(term)
        if not term:
            return ""
        return term

    def list_authors(self):
        out = ""
        num = 1
        for author in self.context.getAuthors():
            out += AUTHOR_TMPL % dict(
                num=num,
                firstname=escape(author["firstname"]),
                lastname=escape(author["lastname"]),
            )
            num += 1
        return out

    def list_editors(self):
        out = ""
        num = 1
        for editor in self.context.getEditorial():
            out += EDITOR_TMPL % dict(
                num=num,
                firstname=escape(editor["firstname"]),
                lastname=escape(editor["lastname"]),
            )
            num += 1
        return out


class XMLRepresentationLZA(XMLRepresentation):
    include_fulltext = True


class XMLRepresentationContainer(XMLRepresentation):
    def __call__(self):
        self.request.response.setHeader("Content-type", "application/zip")
        self.request.response.setHeader(
            "Content-disposition", "inline;filename=%s" % self.filename.encode("utf-8")
        )
        zipdata = self.get_zipdata()
        self.request.response.setHeader("content-length", str(len(zipdata)))
        return zipdata

    def issues(self):
        pc = self.context.portal_catalog
        parent_path = dict(query="/".join(self.context.getPhysicalPath()))
        results = pc(review_state="published", portal_type=("Issue"), path=parent_path)
        for item in results:
            yield item.getObject()

    def write_zipfile(self, zipfile):
        for issue in self.issues():
            xmlview = issue.restrictedTraverse("xml")
            xml = xmlview.template(xmlview)
            filename = xmlview.filename
            zipfile.writestr(filename, bytes(xml.encode("utf-8")))

    def get_zipdata(self):
        stream = BytesIO()
        zipfile = ZipFile(stream, "w")
        self.write_zipfile(zipfile)
        zipfile.close()
        zipdata = stream.getvalue()
        stream.close()
        return zipdata


class XMLRepresentationPublication(XMLRepresentationContainer):
    @property
    def filename(self):
        return "recensio_%s.zip" % (self.get_publication_shortname())


class XMLRepresentationVolume(XMLRepresentationContainer):
    @property
    def filename(self):
        return "recensio_%s_%s.zip" % (
            self.get_publication_shortname(),
            self.get_package_journal_volume(),
        )


class XMLRepresentationIssue(XMLRepresentation):
    template = ViewPageTemplateFile("templates/export_container.pt")

    def __call__(self):
        self.request.response.setHeader("Content-type", "application/xml")
        self.request.response.setHeader(
            "Content-disposition", "inline;filename=%s" % self.filename.encode("utf-8")
        )
        return self.template(self)

    def get_package_journal_pubyear(self):
        return self.get_parent("Volume").getYearOfPublication() or None

    def get_package_journal_issue(self):
        return unicode(self.get_parent("Issue").getId(), "utf-8")

    def get_package_journal_issue_title(self):
        return unicode(self.get_parent("Issue").Title(), "utf-8")

    @property
    def filename(self):
        return "recensio_%s_%s_%s.xml" % (
            self.get_publication_shortname(),
            self.get_package_journal_volume(),
            self.get_package_journal_issue(),
        )

    def reviews(self):
        pc = self.context.portal_catalog
        parent_path = dict(query="/".join(self.context.getPhysicalPath()), depth=3)
        results = pc(
            review_state="published", portal_type=REVIEW_TYPES, path=parent_path
        )
        for item in results:
            yield item.getObject()
