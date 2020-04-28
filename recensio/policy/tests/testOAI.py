# -*- coding: utf-8 -*-
import datetime

import unittest2 as unittest
from recensio.policy.tests.layer import RECENSIO_INTEGRATION_TESTING


class TestOAI(unittest.TestCase):
    layer = RECENSIO_INTEGRATION_TESTING

    def testReader(self):
        from recensio.policy.utility import Reader
        from lxml import etree

        raw_xml = """<?xml version="1.0" encoding="UTF-8" ?>
<?xml-stylesheet type="text/xsl" href="common/xsl/oaicat.xsl"?>
<OAI-PMH xmlns="http://www.openarchives.org/OAI/2.0/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.openarchives.org/OAI/2.0/ http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd">
<responseDate>2010-08-17T15:25:01Z</responseDate>    <request verb="GetRecord" identifier="oai:nature.com:10.1038/scientificamerican0891-40" metadataPrefix="oai_dc">http://www.nature.com/oai/request</request>
<GetRecord>
<record><header><identifier>oai:nature.com:10.1038/scientificamerican0891-40</identifier><datestamp>1991-08-01</datestamp><setSpec>scientificamerican</setSpec></header><metadata><oai_dc:dc xmlns:oai_dc="http://www.openarchives.org/OAI/2.0/oai_dc/" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.openarchives.org/OAI/2.0/oai_dc/ http://www.openarchives.org/OAI/2.0/oai_dc.xsd">
  <dc:identifier>doi:10.1038/scientificamerican0891-40</dc:identifier>
  <dc:title>Colliding Galaxies</dc:title>

  <dc:creator>Joshua Barnes</dc:creator>
  <dc:creator>Lars Hernquist</dc:creator>
  <dc:creator>François Schweizer</dc:creator>
  <dc:publisher>Nature Publishing Group</dc:publisher>
  <dc:date>1991-08-01</dc:date>
  <dc:type>Feature</dc:type>

  <dc:language>en</dc:language>
  <dc:rights>© 1991 Scientific American, Inc.</dc:rights>
</oai_dc:dc></metadata></record></GetRecord>
</OAI-PMH>"""
        root = etree.fromstring(raw_xml)
        expected = {
            "dc_contributor": [],
            "dc_coverage": [],
            "dc_creator": ["Joshua Barnes", "Lars Hernquist", u"Fran\xe7ois Schweizer"],
            "dc_date": [datetime.datetime(1991, 8, 1, 0, 0)],
            "dc_description": [],
            "dc_format": [],
            "dc_identifier": ["doi:10.1038/scientificamerican0891-40"],
            "dc_language": ["en"],
            "dc_publisher": ["Nature Publishing Group"],
            "dc_relation": [],
            "dc_rights": [u"\xa9 1991 Scientific American, Inc."],
            "dc_source": [],
            "dc_subject": [],
            "dc_title": ["Colliding Galaxies"],
            "dc_type": ["Feature"],
            "oai_deleted": False,
            "oai_identifier": "oai:nature.com:10.1038/scientificamerican0891-40",
            "oai_timestamp": datetime.datetime(1991, 8, 1, 0, 0),
            "oai_retrieved": datetime.datetime(2010, 8, 17, 15, 25, 1),
            "oai_sets": [],
        }

        got = Reader()(root)
        self.assertEqual(expected, got)
