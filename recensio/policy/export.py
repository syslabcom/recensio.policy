import tempfile
from DateTime import DateTime
from Products.CMFCore.utils import getToolByName
from datetime import datetime
from datetime import timedelta
from io import FileIO
from os import path
from os import remove
from os import stat
from zipfile import ZipFile
from zope.component.hooks import getSite
from zope.interface import implements
from zope.pagetemplate.pagetemplatefile import PageTemplateFile

from recensio.contenttypes.interfaces.review import IParentGetter
from recensio.policy.interfaces import IRecensioExporter


class StatusSuccess(object):
    value = True


class StatusFailure(object):
    value = False


class StatusSuccessFile(StatusSuccess):

    def __init__(self, filename):
        self.filename = filename


class StatusSuccesFileCreated(StatusSuccessFile):
    pass


class StatusSuccessFileExists(StatusSuccessFile):

    def __init__(self, filename, modified=None):
        self.filename = filename
        self.modified = modified


class StatusFailureAlreadyInProgress(StatusFailure):

    def __init__(self, since=None):
        self.since = since


class ChroniconExporter(object):
    implements(IRecensioExporter)

    template = 'browser/templates/export_container_contextless.pt'
    export_filename = 'export_metadata_xml.zip'

    def __init__(self):
        self.current_issue = None
        self.issues_xml = {}
        self.reviews_xml = []

    def get_parent(self, meta_type):
        if not self.current_issue:
            return None
        return IParentGetter(self.current_issue).get_parent_object_of_type(meta_type)

    def get_publication_shortname(self):
        return unicode(self.get_parent("Publication").getId(), 'utf-8')

    def get_package_journal_volume(self):
        return unicode(self.get_parent("Volume").getId(), 'utf-8')

    def get_package_journal_pubyear(self):
        return self.get_parent("Volume").getYearOfPublication() or None

    def get_package_journal_issue(self):
        return unicode(self.get_parent("Issue").getId(), 'utf-8')

    def get_issue_filename(self):
        return "recensio_%s_%s_%s.xml" % (
            self.get_publication_shortname(),
            self.get_package_journal_volume(),
            self.get_package_journal_issue())

    def finish_issue(self):
        pt = PageTemplateFile(self.template)
        options = {
            'package': {
                'publication_shortname': self.get_publication_shortname,
                'package_journal_volume': self.get_package_journal_volume,
                'package_journal_pubyear': self.get_package_journal_pubyear,
                'package_journal_issue': self.get_package_journal_issue,
            },
            'reviews': self.reviews_xml,
        }
        filename = self.get_issue_filename()
        xml = pt(**options)
        self.issues_xml[filename] = xml
        self.reviews = []
        self.current_issue = None

    @property
    def cache_filename(self):
        return path.join(tempfile.gettempdir(), 'recensio_cached_all.zip')

    def write_zipfile(self, zipfile):
        for filename, xml in self.issues_xml.items():
            zipfile.writestr(filename, bytes(xml.encode('utf-8')))

    def get_zipdata(self):
        cache_file_name = self.cache_filename
        stream = FileIO(cache_file_name, mode='w')
        zipfile = ZipFile(stream, 'w')
        self.write_zipfile(zipfile)
        zipfile.close()
        stream.close()

        stream = FileIO(cache_file_name, mode='r')
        zipdata = stream.readall()
        stream.close()
        remove(cache_file_name)
        return zipdata

    def get_export_obj(self, portal):
        try:
            export_xml = portal.unrestrictedTraverse(
                self.export_filename)
        except (KeyError, ValueError):
            export_xml = None
        return export_xml

    def add_review(self, review):
        review_issue = IParentGetter(review).get_parent_object_of_type('Issue')
        if self.current_issue != review_issue:
            if self.current_issue:
                self.finish_issue()
            self.current_issue = review_issue
        self.reviews_xml.append(review.restrictedTraverse('@@xml')())

    def export(self):
        if self.current_issue:
            self.finish_issue()

        portal = getSite()
        export_xml = self.get_export_obj(portal)
        if export_xml is not None:
            modified = export_xml.modified()
            if DateTime() - 7 < modified:
                return StatusSuccessFileExists(
                    self.export_filename, modified.ISO8601())
        if path.exists(self.cache_filename):
            mtime = stat(self.cache_filename).st_mtime
            cache_time = datetime.fromtimestamp(mtime)
            if datetime.now() - cache_time < timedelta(0, 60 * 60):
                return StatusFailureAlreadyInProgress(
                    cache_time.isoformat())

        pt = getToolByName(portal, 'portal_types')
        type_info = pt.getTypeInfo('File')
        export_xml = type_info._constructInstance(
            portal, self.export_filename)
        export_xml.setFile(self.get_zipdata(), filename=self.export_filename)
        return StatusSuccesFileCreated(self.export_filename)
