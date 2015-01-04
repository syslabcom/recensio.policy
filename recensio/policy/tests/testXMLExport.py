import re
import unittest2 as unittest
from collective.solr.interfaces import ISolrConnectionConfig
from io import BytesIO
from plone import api
from plone.app.testing.helpers import login
from plone.app.testing.interfaces import SITE_OWNER_NAME
from plone.app.testing.interfaces import TEST_USER_NAME
from zipfile import ZipFile

from recensio.policy.export import ChroniconExporter
from recensio.policy.export import StatusSuccessFile
from recensio.policy.tests.layer import RECENSIO_INTEGRATION_TESTING


class TextExporter(unittest.TestCase):
    layer = RECENSIO_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        summer_a = self.portal['sample-reviews']['newspapera']['summer']
        issue_2_a = summer_a['issue-2']
        summer_b = self.portal['sample-reviews']['newspaperb']['summer']
        issue_2_b = summer_b['issue-2']
        self.review_a = issue_2_a.objectValues()[0]
        self.review_b = issue_2_b.objectValues()[0]

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
        xml_data = export_zip.read('recensio_newspapera_summer_issue-2.xml')
        self.assertIn('<issue_recensio_package', xml_data)
        self.assertIn('<title>' + self.review_a.Title() + '</title>', xml_data)
        self.assertNotIn('<title>' + self.review_b.Title() + '</title>', xml_data)
        xml_data = export_zip.read('recensio_newspaperb_summer_issue-2.xml')
        self.assertIn('<title>' + self.review_b.Title() + '</title>', xml_data)


class TestXMLExport(unittest.TestCase):
    layer = RECENSIO_INTEGRATION_TESTING

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
        api.content.transition(obj=self.review_1, to_state='published')

        login(self.portal, TEST_USER_NAME)

    def tearDown(self):
        if self.solrcfg:
            self.solrcfg.active = self.old_solrcfg_active

    def _force_fresh_export_run(self):
        xml_export = self.portal.restrictedTraverse('@@xml-export')
        output = xml_export()
        if 'found' in output:
            match = re.match('.*\((.*), .*\)', output)
            old_export_zip = self.portal[match.group(1)]
            login(self.layer['app'], SITE_OWNER_NAME)
            api.content.delete(old_export_zip)
            login(self.portal, TEST_USER_NAME)
            output = xml_export()
        return output

    def test_export(self):
        output = self._force_fresh_export_run()
        self.assertIn('created', output)

        filename = output.split(' ')[0]
        export_file = self.portal[filename]
        fp = export_file.getFile().getBlob().open()
        export_zip = ZipFile(fp)
        self.assertIn('recensio_newspapera_summer_issue-2.xml',
                      [f.filename for f in export_zip.filelist])
        xml_data = export_zip.read('recensio_newspapera_summer_issue-2.xml')
        self.assertIn('<issue_recensio_package', xml_data)
        self.assertIn('<title>' + self.review_1.Title() + '</title>', xml_data)
        self.assertIn('<rm id="' + self.review_1.UID() + '">', xml_data)
        self.assertIn('<bvid>' + self.review_1.getBv() + '</bvid>', xml_data)
        #TODO: assert full text not contained
