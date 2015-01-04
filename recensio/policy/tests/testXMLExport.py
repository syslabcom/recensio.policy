import re
import unittest2 as unittest
from collective.solr.interfaces import ISolrConnectionConfig
from zipfile import ZipFile
from plone import api
from plone.app.testing.helpers import login
from plone.app.testing.interfaces import SITE_OWNER_NAME
from plone.app.testing.interfaces import TEST_USER_NAME

from recensio.policy.tests.layer import RECENSIO_INTEGRATION_TESTING


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
        issue_2 = self.portal['sample-reviews']['newspapera']['summer']['issue-2']
        api.content.transition(obj=issue_2, to_state='published')
        self.review_1 = issue_2.objectValues()[0]
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
        #TODO: assert full text not contained
