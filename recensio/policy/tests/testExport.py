# -*- coding: utf-8 -*-
import os
import unittest2 as unittest
from StringIO import StringIO
from collective.solr.interfaces import ISolrConnectionConfig
from lxml import etree
from mock import Mock
from plone import api
from plone.app.testing.helpers import login
from plone.app.testing.interfaces import SITE_OWNER_NAME
from plone.app.testing.interfaces import TEST_USER_NAME
from zipfile import ZipFile
from recensio.policy.interfaces import IRecensioExporter
from time import time
from zope.annotation.interfaces import IAnnotations
from zope.component import getFactoriesFor
from zope.component import getGlobalSiteManager
from zope.component.factory import Factory
from zope.component.interfaces import IFactory
from zope.interface import implements

from recensio.contenttypes.setuphandlers import add_number_of_each_review_type
from recensio.contenttypes.content.reviewmonograph import ReviewMonograph
from recensio.policy.browser.export import EXPORT_TIMESTAMP_KEY
from recensio.policy.export import BVIDExporter
from recensio.policy.export import ChroniconExporter
from recensio.policy.export import DaraExporter
from recensio.policy.export import MissingBVIDExporter
from recensio.policy.export import StatusFailure
from recensio.policy.export import StatusSuccessFile
from recensio.policy.tests.layer import RECENSIO_FUNCTIONAL_TESTING
from recensio.policy.tests.layer import RECENSIO_BARE_INTEGRATION_TESTING


class BrokenExporter(object):
    implements(IRecensioExporter)

    def needs_to_run(self):
        return True

    def add_review(self, review):
        raise Exception('some error')

    def export(self):
        return StatusFailure()


class TestExporter(unittest.TestCase):
    layer = RECENSIO_BARE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

        login(self.layer['app'], SITE_OWNER_NAME)
        add_number_of_each_review_type(
            self.portal, 1, rez_classes=[ReviewMonograph])
        login(self.portal, TEST_USER_NAME)

        summer_a = self.portal['sample-reviews']['newspapera']['summer']
        issue_2_a = summer_a['issue-2']
        summer_b = self.portal['sample-reviews']['newspaperb']['summer']
        issue_2_b = summer_b['issue-2']
        self.review_a = issue_2_a.objectValues()[0]
        self.review_b = issue_2_b.objectValues()[0]

    def assertValid(self, xml, schema_name):
        schemafile = open(os.path.join(
            os.path.dirname(__file__),
            schema_name))
        xmlschema = etree.XMLSchema(etree.parse(schemafile))
        schemafile.close()
        xmlschema.assertValid(xml)

    def test_dara_exporter(self):
        exporter = DaraExporter()
        exporter.add_review(self.review_a)
        self.assertEqual(len(exporter.reviews_xml), 1)
        xml = exporter.reviews_xml[0]
        xmltree = etree.parse(StringIO(xml.encode('utf8')))

        self.assertValid(xmltree, 'dara_v3.1_de_en_18112014.xsd')
        self.assertIn(
            self.review_a.UID(),
            xmltree.xpath('/resource/resourceIdentifier/identifier/text()'))
        self.assertEqual(
            len(xmltree.xpath('/resource/titles/title')),
            1)
        self.assertIn(
            u'Rezension über ' + self.review_a.Title(),
            xmltree.xpath('/resource/titles/title/titleName/text()'))
        self.assertIn(
            self.review_a.getAuthors()[0]['firstname'],
            xmltree.xpath('/resource/creators/creator/person/firstName/text()'))
        self.assertIn(
            self.review_a.getAuthors()[0]['lastname'],
            xmltree.xpath('/resource/creators/creator/person/lastName/text()'))
        self.assertIn(
            self.review_a.absolute_url(),
            xmltree.xpath('/resource/dataURLs/dataURL/text()'))
        self.assertIn(
            'CC-BY',
            '\n'.join(xmltree.xpath('/resource/rights/right/rightsText/text()')))
        status = exporter.export()

    def test_chronicon_exporter_one_issue(self):
        exporter = ChroniconExporter()
        exporter.add_review(self.review_a)
        status = exporter.export()
        self.assertTrue(isinstance(status, StatusSuccessFile))
        filename = status.filename
        export_file = self.portal[filename]
        fp = export_file.getFile().getBlob().open()
        export_zip = ZipFile(fp)

        self.assertIn('recensio_newspapera_summer_issue-2.xml',
                      [f.filename for f in export_zip.filelist])
        xml_data = export_zip.read('recensio_newspapera_summer_issue-2.xml')
        self.assertIn('<issue_recensio_package', xml_data)
        self.assertIn('<title>' + self.review_a.Title() + '</title>', xml_data)
        self.assertIn('<rm id="' + self.review_a.UID() + '">', xml_data)
        #TODO: assert full text not contained

    def test_chronicon_exporter_two_issues(self):
        exporter = ChroniconExporter()
        exporter.add_review(self.review_a)
        exporter.add_review(self.review_b)
        status = exporter.export()
        self.assertTrue(isinstance(status, StatusSuccessFile))
        filename = status.filename
        export_file = self.portal[filename]
        fp = export_file.getFile().getBlob().open()
        export_zip = ZipFile(fp)

        self.assertIn('recensio_newspapera_summer_issue-2.xml',
                      [f.filename for f in export_zip.filelist])
        self.assertIn('recensio_newspaperb_summer_issue-2.xml',
                      [f.filename for f in export_zip.filelist])

        xml_data = export_zip.read('recensio_newspaperb_summer_issue-2.xml')
        self.assertIn('<issue_recensio_package', xml_data)
        self.assertIn('<title>' + self.review_b.Title() + '</title>', xml_data)
        self.assertNotIn('<title>' + self.review_a.Title() + '</title>', xml_data)

        xml_data = export_zip.read('recensio_newspapera_summer_issue-2.xml')
        self.assertIn('<title>' + self.review_a.Title() + '</title>', xml_data)
        self.assertNotIn('<title>' + self.review_b.Title() + '</title>', xml_data)

    def test_bvid_exporter(self):
        self.review_b.setBv('12345')
        exporter = BVIDExporter()
        exporter.add_review(self.review_a)
        exporter.add_review(self.review_b)
        status = exporter.export()
        self.assertTrue(isinstance(status, StatusSuccessFile))

        filename = status.filename
        export_file = self.portal[filename]
        fp = export_file.getFile().getBlob().open()
        csv_data = fp.read()
        self.assertIn(self.review_b.getBv(), csv_data)

        self.review_b.setBv('')

    def test_missing_bvid_exporter(self):
        exporter = MissingBVIDExporter()
        exporter.add_review(self.review_a)
        exporter.add_review(self.review_b)
        status = exporter.export()
        self.assertTrue(isinstance(status, StatusSuccessFile))

        filename = status.filename
        export_file = self.portal[filename]
        fp = export_file.getFile().getBlob().open()
        csv_data = fp.read()
        self.assertIn(self.review_a.absolute_url(), csv_data)


class TestMetadataExport(unittest.TestCase):
    layer = RECENSIO_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        sm = self.portal.getSiteManager()
        self.solrcfg = None
        solrcfgs = sm.getAllUtilitiesRegisteredFor(ISolrConnectionConfig)
        if not len(solrcfgs) == 0:
            self.solrcfg = solrcfgs[0]
            self.old_solrcfg_active = self.solrcfg.active
            # Workaround. The publish operation below is not reflected in Solr
            self.solrcfg.active = False

        login(self.layer['app'], SITE_OWNER_NAME)
        summer = self.portal['sample-reviews']['newspapera']['summer']
        issue_2 = summer['issue-2']
        api.content.transition(obj=issue_2, to_state='published')
        self.review_1 = issue_2.objectValues()[0]
        self.review_1.setBv('12345')
        self.review_1.setCanonical_uri(u'http://example.com/reviews/review1')
        api.content.transition(obj=self.review_1, to_state='published')

        login(self.portal, TEST_USER_NAME)
        self.xml_export = self.portal.restrictedTraverse('@@metadata-export')

    def tearDown(self):
        self.review_1.setBv('')
        self.review_1.setCanonical_uri(u'')
        if self.solrcfg:
            self.solrcfg.active = self.old_solrcfg_active

    def _clear_export_files(self):
        login(self.layer['app'], SITE_OWNER_NAME)
        exporters = [factory() for name, factory in
                     getFactoriesFor(IRecensioExporter)]
        for exporter in exporters:
            old_export_file = self.portal.get(exporter.export_filename)
            if old_export_file:
                api.content.delete(old_export_file)
        login(self.portal, TEST_USER_NAME)

    def test_export(self):
        self._clear_export_files()
        output = self.xml_export()
        self.assertIn('created', output)

        for line in output.split('\n'):
            if 'chronicon' in line:
                filename = line.split(' ')[1]
        export_file = self.portal[filename]
        fp = export_file.getFile().getBlob().open()
        export_zip = ZipFile(fp)
        self.assertIn('recensio_newspapera_summer_issue-2.xml',
                      [f.filename for f in export_zip.filelist])
        xml_data = export_zip.read('recensio_newspapera_summer_issue-2.xml')
        self.assertIn('<issue_recensio_package', xml_data)
        self.assertIn('<title>' + self.review_1.Title() + '</title>', xml_data)
        self.assertIn('<rm id="' + self.review_1.UID() + '">', xml_data)
        self.assertIn('<page_first>' + str(self.review_1.getPageStartOfReviewInJournal()) + '</page_first>', xml_data)
        self.assertIn('<page_last>' + str(self.review_1.getPageEndOfReviewInJournal()) + '</page_last>', xml_data)
        self.assertIn('<originalurl>' + self.review_1.getCanonical_uri() + '</originalurl>', xml_data)
        #TODO: assert full text not contained

        output = self.xml_export()
        self.assertIn('Nothing to do', output)

    def test_broken_exporter_not_fatal(self):
        gsm = getGlobalSiteManager()
        factory = Factory(BrokenExporter, IFactory, 'broken_exporter')
        gsm.registerUtility(
            factory,
            name='broken')
        output = self.xml_export()
        self.assertIn('broken', output)
        gsm.unregisterUtility(
            factory,
            name='broken')

    def test_export_sets_timestamp(self):
        from recensio.policy.browser.export import MetadataExport

        def mock_issues(_self):
            annotations = IAnnotations(self.portal)
            self.assertIn(EXPORT_TIMESTAMP_KEY, annotations)
            return []
        _issues = MetadataExport.issues
        MetadataExport.issues = mock_issues

        self._clear_export_files()
        self.xml_export()

        MetadataExport.issues = _issues

    def test_timestamp_prevents_export_run(self):
        from recensio.policy.browser.export import MetadataExport
        _issues = MetadataExport.issues
        mock_issues = Mock(return_value=[])
        MetadataExport.issues = mock_issues

        annotations = IAnnotations(self.portal)
        # fake running export
        annotations[EXPORT_TIMESTAMP_KEY] = time()
        self._clear_export_files()
        output = self.xml_export()
        self.assertFalse(mock_issues.called)
        self.assertIn('abort', output)

        mock_issues.reset_mock()
        # fake running export has finished
        del annotations[EXPORT_TIMESTAMP_KEY]
        self._clear_export_files()
        output = self.xml_export()
        self.assertTrue(mock_issues.called)
        self.assertNotIn('abort', output)

        if EXPORT_TIMESTAMP_KEY in annotations:
            del annotations[EXPORT_TIMESTAMP_KEY]
        MetadataExport.issues = _issues

    def test_timestamp_not_left_behind(self):
        from recensio.policy.browser.export import MetadataExport
        _issues = MetadataExport.issues
        mock_issues = Mock(return_value=[])
        MetadataExport.issues = mock_issues

        annotations = IAnnotations(self.portal)

        self._clear_export_files()
        output = self.xml_export()
        self.assertTrue(mock_issues.called)
        self.assertNotIn('abort', output)

        mock_issues.reset_mock()
        # recent run should not have left behind a time stamp
        self._clear_export_files()
        output = self.xml_export()
        self.assertTrue(mock_issues.called)
        self.assertNotIn('abort', output)

        if EXPORT_TIMESTAMP_KEY in annotations:
            del annotations[EXPORT_TIMESTAMP_KEY]
        MetadataExport.issues = _issues

    def test_timestamp_not_left_behind_by_noop_export(self):
        annotations = IAnnotations(self.portal)

        self._clear_export_files()
        # regular export run
        output = self.xml_export()

        # we don't care about the time stamp at this point, this is tested in
        # another test
        if EXPORT_TIMESTAMP_KEY in annotations:
            del annotations[EXPORT_TIMESTAMP_KEY]
        # not clearing files - this export has nothing to do
        output = self.xml_export()

        # the most recent export should not have left behind a time stamp
        output = self.xml_export()
        self.assertNotIn('abort', output)

        if EXPORT_TIMESTAMP_KEY in annotations:
            del annotations[EXPORT_TIMESTAMP_KEY]

    def test_stale_timestamp_is_cleared(self):
        from recensio.policy.browser.export import MetadataExport
        _issues = MetadataExport.issues
        mock_issues = Mock(return_value=[])
        MetadataExport.issues = mock_issues

        annotations = IAnnotations(self.portal)
        # fake a four day old stale time stamp
        annotations[EXPORT_TIMESTAMP_KEY] = time() - 4 * 60 * 60
        self._clear_export_files()
        output = self.xml_export()
        self.assertTrue(mock_issues.called)
        self.assertNotIn('abort', output)

        if EXPORT_TIMESTAMP_KEY in annotations:
            del annotations[EXPORT_TIMESTAMP_KEY]
        MetadataExport.issues = _issues
