import csv
import tempfile
from Acquisition import aq_parent
from DateTime import DateTime
from Products.CMFCore.utils import getToolByName
from StringIO import StringIO
from Testing.makerequest import makerequest
from base64 import b64encode
from datetime import datetime
from datetime import timedelta
from io import FileIO
from os import path
from os import remove
from os import stat
from plone import api
from plone.registry.interfaces import IRegistry
from urllib2 import Request
from urllib2 import urlopen
from zipfile import ZipFile
from zope.component import queryUtility
from zope.component.factory import Factory
from zope.component.hooks import getSite
from zope.component.interfaces import IFactory
from zope.interface import implements
from zope.pagetemplate.pagetemplatefile import PageTemplateFile

from recensio.contenttypes.interfaces.review import IParentGetter
from recensio.policy.interfaces import IRecensioExporter
from recensio.policy.interfaces import IRecensioSettings


class StatusSuccess(object):
    value = True

    def __repr__(self):
        return 'Success'


class StatusFailure(object):
    value = False

    def __repr__(self):
        return 'Failure'


class StatusSuccessFile(StatusSuccess):

    def __init__(self, filename):
        self.filename = filename


class StatusSuccessFileCreated(StatusSuccessFile):

    def __repr__(self):
        return "{0} created".format(self.filename)


class StatusSuccessFileExists(StatusSuccessFile):

    def __init__(self, filename, modified=None):
        self.filename = filename
        self.modified = modified

    def __repr__(self):
        return 'current file found ({0}, {1})'.format(
            self.filename, self.modified)


class StatusFailureAlreadyInProgress(StatusFailure):

    def __init__(self, since=None):
        self.since = since

    def __repr__(self):
        return 'export in progress since {0}'. format(self.since)


class BaseExporter(object):

    def get_export_obj(self, portal):
        try:
            export_xml = portal.unrestrictedTraverse(
                self.export_filename)
        except (KeyError, ValueError):
            export_xml = None
        return export_xml

    def is_recent(self, export_xml_obj):
        if export_xml_obj is not None:
            modified = export_xml_obj.modified()
            if DateTime() - 7 < modified:
                return True
        return False


class ChroniconExporter(BaseExporter):
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

    def get_publication_title(self):
        return unicode(self.get_parent("Publication").Title(), 'utf-8')

    def get_package_journal_volume(self):
        return unicode(self.get_parent("Volume").getId(), 'utf-8')

    def get_package_journal_volume_title(self):
        return unicode(self.get_parent("Volume").Title(), 'utf-8')

    def get_package_journal_pubyear(self):
        return self.get_parent("Volume").getYearOfPublication() or None

    def get_package_journal_issue(self):
        return unicode(self.get_parent("Issue").getId(), 'utf-8')

    def get_package_journal_issue_title(self):
        return unicode(self.get_parent("Issue").Title(), 'utf-8')

    def get_issue_filename(self):
        return "recensio_%s_%s_%s.xml" % (
            self.get_publication_shortname(),
            self.get_package_journal_volume(),
            self.get_package_journal_issue())

    def finish_issue(self):
        pt = PageTemplateFile(self.template)
        options = {
            'package': {
                'publication_title': self.get_publication_title,
                'package_journal_volume_title': self.get_package_journal_volume_title,
                'package_journal_pubyear': self.get_package_journal_pubyear,
                'package_journal_issue_title': self.get_package_journal_issue_title,
            },
            'reviews': self.reviews_xml,
        }
        filename = self.get_issue_filename()
        xml = pt(**options)
        self.issues_xml[filename] = xml
        self.reviews_xml = []
        self.current_issue = None

    @property
    def cache_filename(self):
        return path.join(tempfile.gettempdir(), 'chronicon_cache.zip')

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

    def running_export(self):
        if path.exists(self.cache_filename):
            mtime = stat(self.cache_filename).st_mtime
            cache_time = datetime.fromtimestamp(mtime)
            if datetime.now() - cache_time < timedelta(0, 60 * 60):
                return cache_time

    def needs_to_run(self):
        portal = getSite()
        export_xml_obj = self.get_export_obj(portal)
        return not self.is_recent(export_xml_obj) and not self.running_export()

    def add_review(self, review):
        """Expects reviews of the same issue to be added consecutively"""
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
        export_xml_obj = self.get_export_obj(portal)
        cache_time = self.running_export()
        if cache_time:
            return StatusFailureAlreadyInProgress(
                cache_time.isoformat())

        pt = getToolByName(portal, 'portal_types')
        type_info = pt.getTypeInfo('File')
        if export_xml_obj is None:
            export_xml_obj = type_info._constructInstance(
                portal, self.export_filename)
        export_xml_obj.setFile(self.get_zipdata(),
                               filename=self.export_filename)
        export_xml_obj.setModificationDate(DateTime())
        return StatusSuccessFileCreated(self.export_filename)


class BVIDExporter(BaseExporter):
    implements(IRecensioExporter)

    export_filename = 'bvid_export.csv'

    def __init__(self):
        self.items = []

    def needs_to_run(self):
        portal = getSite()
        export_file = self.get_export_obj(portal)
        return not self.is_recent(export_file)

    def add_review(self, review):
        if review.getBv():
            self.items.append((review.getBv(), review.absolute_url()))

    def export(self):
        csvfile = StringIO()
        csvwriter = csv.writer(csvfile)

        csvwriter.writerows(self.items)

        portal = getSite()
        export_file = self.get_export_obj(portal)
        if export_file is None:
            pt = getToolByName(portal, 'portal_types')
            type_info = pt.getTypeInfo('File')
            export_file = type_info._constructInstance(
                portal, self.export_filename)

        export_file.setFile(csvfile.getvalue(), filename=self.export_filename)
        export_file.setModificationDate(DateTime())
        return StatusSuccessFileCreated(self.export_filename)


class MissingBVIDExporter(BVIDExporter):
    implements(IRecensioExporter)

    export_filename = 'missing_bvid.csv'

    def add_review(self, review):
        if not review.getBv():
            self.items.append((review.Title(), review.absolute_url()))


class DaraExporter(BaseExporter):

    def __init__(self):
        self.reviews_xml = []

    def add_review(self, review):
        self.reviews_xml.append(review.restrictedTraverse('@@xml-dara')())

    def export(self):
        pass

BVIDExporterFactory = Factory(
    BVIDExporter, IFactory, 'exporter')
MissingBVIDExporterFactory = Factory(
    MissingBVIDExporter, IFactory, 'exporter')
ChroniconExporterFactory = Factory(
    ChroniconExporter, IFactory, 'exporter')


def register_doi(obj):
    registry = queryUtility(IRegistry)
    settings = registry.forInterface(IRecensioSettings)
    username = settings.doi_registration_username
    password = settings.doi_registration_password
    auth = b64encode('{0}:{1}'.format(username, password))
    url = settings.doi_registration_url.encode('utf-8')

    xml = obj.restrictedTraverse('@@xml-dara')().encode('utf-8')
    headers = {
        'Content-type': 'application/xml;charset=UTF-8',
        'Authorization': 'Basic ' + auth}
    result = urlopen(Request(url, xml, headers))
    return_code = result.getcode()
    result.close()
    return return_code


def register_doi_requestless(obj, portal_url):
    portal = api.portal.get()
    app = aq_parent(portal)
    app = makerequest(app, environ=dict(SERVER_URL=portal_url))
    app.REQUEST.other['PARENTS'] = [portal, app]
    app.REQUEST.other['VirtualRootPhysicalPath'] = ('', portal.id)
    portal.REQUEST = app.REQUEST

    result = register_doi(obj)
    delattr(portal, 'REQUEST')
    return result
