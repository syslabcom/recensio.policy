# -*- coding: utf-8 -*-
from zope.testing.loggingsupport import InstalledHandler

import logging
import os
import sparql
import unittest2 as unittest
from StringIO import StringIO
from mock import patch


class MockResultFactory(object):
    def __init__(self, filename):
        mock_data_file = open(os.path.join(os.path.dirname(__file__), filename), 'r')
        self.mock_data = mock_data_file.read()
        mock_data_file.close()

    def __call__(self, dummy):
        return sparql._ResultsParser(StringIO(self.mock_data))


#TODO: Also mock away the request in recensio.policy.sparqlsearch.graph_parse()?
# def mock_graph_parse(iri, **kw):
#     return "[a rdfg:Graph;rdflib:storage [a rdflib:Store;rdfs:label 'IOMemory']]"


class TestSparqlBase(unittest.TestCase):

    def setUp(self):
        self.handler = InstalledHandler('recensio', level=logging.DEBUG)
        self.maxDiff = None

    def tearDown(self):
        self.handler.uninstall()


class TestSparqlStable(TestSparqlBase):

    def testGetLabels(self):
        from rdflib.graph import Graph
        from recensio.policy.sparqlsearch import getLabels
        graph = Graph()
        test_url = 'http://id.loc.gov/vocabulary/iso639-2/und'
        graph.parse(test_url)
        expected = {
            u'de': u'Nicht Zu Entscheiden',
            u'fr': u'Ind\xe9termin\xe9e',
            u'en': u'Undetermined',
        }
        self.assertEquals(expected, getLabels(test_url, graph))

    def testSeriesVolumeStore(self):
        returnval = {
            'series': None,
            'seriesVol': None,
        }

        class mockCitation(object):
            value = 'Oldenbourg-Grundriss der Geschichte : 23'
        obj = mockCitation()

        from recensio.policy.sparqlsearch import seriesVolumeStore
        seriesVolumeStore(obj, returnval)
        self.assertEquals(
            returnval['series'],
            'Oldenbourg-Grundriss der Geschichte')
        self.assertEquals(returnval['seriesVol'], '23')

    def testSeriesVolumeStoreMultipleEntries(self):
        returnval = {
            'series': None,
            'seriesVol': None,
        }

        class mockCitation(object):
            value = ''

            def __init__(self, value):
                self.value = value

        obj1 = mockCitation('Oldenbourg-Grundriss der Geschichte : 23')
        obj2 = mockCitation(u'Schriften der Bibliothek für Zeitgeschichte '
                            u': Neue Folge : 22')
        obj3 = mockCitation('Oldenbourg-Grundriss der Geschichte : 23')

        from recensio.policy.sparqlsearch import seriesVolumeStore
        seriesVolumeStore(obj1, returnval)
        seriesVolumeStore(obj2, returnval)
        seriesVolumeStore(obj3, returnval)
        self.assertEquals(
            returnval['series'],
            u'Oldenbourg-Grundriss der Geschichte; '
            u'Schriften der Bibliothek für Zeitgeschichte : Neue Folge')
        self.assertEquals(returnval['seriesVol'], '23; 22')

    def testGetEmptyMetadata(self):
        from recensio.policy.sparqlsearch import getMetadata
        # http://lod.b3kat.de/title/BV013575871

        expected = {
            'bv': u'BV013575871',
            'ddcSubject': [],
            'isbn': u'123',
            'keywords': [],
            'language': u'English',
            'location': u'K\xf8benhavn',
            'pages': u'223',
            'publisher': None,
            'series': u'2; Grønlands Geologiske Undersøgelse: Bulletin',
            'seriesVol': u'25',
            'subtitle': None,
            'title': u'Structural studies in the Pre-Cambrian of western Greenland',
            'year': u'1960',
        }

        mock_config = {'side_effect': MockResultFactory('sparql_data_no_metadata.xml')}
        with patch('sparql.Service.query', **mock_config):
            is_ = getMetadata('123')
        is_.pop('authors')

        ignored = sorted([
            u"We ignore the following information: 'http://id.loc.gov/vocabulary/relators/aut', Content: 'http://d-nb.info/gnd/116149027'",
            u"We ignore the following information: 'http://iflastandards.info/ns/isbd/elements/P1053', Content: '223 S. Ill., Kt. 4 Kt.'",
            u"We ignore the following information: 'http://purl.org/dc/terms/description', Content: 'SA aus: Meddelelser om Gronland ; 123,1'",
            u"We ignore the following information: 'http://purl.org/dc/terms/description', Content: 'by Asger Berthelsen'",
            u"We ignore the following information: 'http://purl.org/dc/terms/isPartOf', Content: 'http://lod.b3kat.de/title/BV000898335'",
            u"We ignore the following information: 'http://purl.org/dc/terms/isPartOf', Content: 'http://lod.b3kat.de/title/BV013568231'",
            u"We ignore the following information: 'http://purl.org/ontology/bibo/oclcnum', Content: '312158810'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-11/item/BV013575871'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-188/item/BV013575871'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-19/item/BV013575871'",
            u"We ignore the following information: 'http://rdvocab.info/Elements/otherTitleInformation', Content: '2: Geology of Tovqussap Nun\xe1'",
            u"We ignore the following information: 'http://rdvocab.info/Elements/publicationStatement', Content: 'K\xf8benhavn 1960'",
            u"We ignore the following information: 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', Content: 'http://purl.org/dc/dcmitype/Text'",
            u"We ignore the following information: 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', Content: 'http://purl.org/ontology/bibo/Book'",
            u"We ignore the following information: 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', Content: 'http://purl.org/ontology/bibo/Document'",
            u"We ignore the following information: 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', Content: 'http://purl.org/ontology/bibo/Thesis'",
            u"We ignore the following information: 'http://www.w3.org/2002/07/owl#sameAs', Content: 'http://hub.culturegraph.org/about/BVB-BV013575871'",
        ])

        errors = sorted([x.msg % x.args for x in self.handler.records
                         if not x.msg.startswith("Sparql query")])

        self.assertEquals(ignored, errors)

        self.assertEquals(expected, is_)

    def testExpectedMetadata01(self):
        from recensio.policy.sparqlsearch import getMetadata
        mock_config = {'side_effect': MockResultFactory('sparql_data_01.xml')}
        with patch('sparql.Service.query', **mock_config):
            result = getMetadata('9783830921929')
        # http://lod.b3kat.de/title/BV035724519

        expected = {
            'bv': u'BV035724519',
            'authors': [],
            'ddcSubject': [u'372.6049'],
            'isbn': u'9783830921929',
            'keywords': [
                u'Kindertagessta\u0308Tte',
                u'Kindertagesst\xe4tte',
                u'Kindertagesst\xe4tte - Spracherziehung - Kongress - Recklinghausen <2008>',
                u'Kongress',
                u'Recklinghausen <2008>',
                u'Spracherziehung',
            ],
            'language': u'German',
            'location': u'M\xfcnster ; New York NY ; M\xfcnchen ; Berlin',
            'pages': u'162',
            'publisher': u'Waxmann',
            'series': None,
            'seriesVol': None,
            'subtitle': u'Sprachentwicklung und Sprachf\xf6rderung in Kindertagesst\xe4tten ; [anl\xe4sslich des Landeskongresses \"Kinder Bilden Sprache - Sprache Bildet Kinder\" am 4. November 2008 in Recklinghausen]',
            'title': u'Kinder bilden Sprache - Sprache bildet Kinder',

            'year': u'2009',
        }
        self.assertEquals(expected, result)

    def testExpectedMetadata02(self):
        from recensio.policy.sparqlsearch import getMetadata
        mock_config = {'side_effect': MockResultFactory('sparql_data_02.xml')}
        with patch('sparql.Service.query', **mock_config):
            metadata = getMetadata('978-0-19-928007-0')

        expected = {
            'bv': u'BV035356471',
            'authors': [],
            'ddcPlace': [u'43'],
            'ddcSubject': [u'900', u'943.085'],
            'ddcTime': [u'09042'],
            'isbn': u'9780199280070',
            'keywords': [
                u'Deutschland',
                u'Germany',
                u'Geschichte 1918-1933',
                u'Weimarer Republik',
            ],
            'language': u'English',
            'location': u'Oxford [u.a.], United Kingdom',
            'pages': u'324',
            'publisher': u'Oxford Univ. Press',
            'series': u'\x98The\x9c short Oxford history of Germany',
            'seriesVol': None,
            'subtitle': None,
            'title': u'Weimar Germany',
            'year': u'2010',
        }
        self.assertEquals(expected, metadata)


class TestSparqlUnstable(TestSparqlBase):
    """ These tests break repeatedly, but may serve some use as
    documentation. They can be run run with `./bin/test -all `"""
    level = 100

    def testExpectedMetadata03(self):
        from recensio.policy.sparqlsearch import getMetadata
        mock_config = {'side_effect': MockResultFactory('sparql_data_03.xml')}
        with patch('sparql.Service.query', **mock_config):
            metadata = getMetadata('9783898617277')

        expected = {
            'authors': [],
            'bv': u'BV023169149',
            'ddcSubject': [u'355.009', u'940.3'],
            'ddcPlace': [u'181'],
            'ddcTime': [u'09041'],
            'isbn': u'9783898617277',
            'keywords': [
                u'Aufsatzsammlung', u'Geschichte',
                u'Kollektives Geda\u0308Chtnis',
                u'Kollektives Ged\xe4chtnis',
                u'Weltkrieg <1914-1918>',
            ],
            'language': u'German',
            'location': u'Essen, Germany',
            'pages': u'222',
            'publisher': u'Klartext',
            'series': u'Schriften der Bibliothek für Zeitgeschichte '
                      ': Neue Folge',
            'seriesVol': u'22',
            'subtitle': None,
            'title': u'\x98Der\x9c Erste Weltkrieg in der popul\xe4ren Erinnerungskultur',
            'year': u'2008',
        }
        self.assertEquals(expected, metadata)

    def testGetMetadata04(self):
        expected = {
            'bv': u'BV039685251',
            'authors': [{'firstname': u'Konrad', 'lastname': u'Canis'},
                   {'firstname': u'Michael', 'lastname': u'Epkenhans'},
                {'firstname': u'Otto', 'lastname': u'Bismarck'}],
            'ddcSubject': [],
            'isbn': u'9783506770707',
            'keywords': [u'Deutschland', u'Politik', u'Quelle'],
            'language': u'German',
            'location': u'Germany',
            'pages': u'616',
            'publisher': u'Sch\xf6ningh',
            'series': None,
            'seriesVol': None,
            'subtitle': None,
            'title': u'Gesammelte Werke',
            'year': u'2012',
        }

        ignored = sorted([
            u"We ignore the following information: 'http://id.loc.gov/vocabulary/relators/ctb', Content: 'http://d-nb.info/gnd/122558316'",
            u"We ignore the following information: 'http://id.loc.gov/vocabulary/relators/ctb', Content: 'http://d-nb.info/gnd/135947308'",
            u"We ignore the following information: 'http://iflastandards.info/ns/isbd/elements/P1053', Content: 'XXXI, 616 S. Ill.'",
            u"We ignore the following information: 'http://purl.org/dc/terms/description', Content: 'Otto von Bismarck Hrsg von Konrad Canis'",
            u"We ignore the following information: 'http://purl.org/dc/terms/isPartOf', Content: 'http://lod.b3kat.de/title/BV017995925'",
            u"We ignore the following information: 'http://purl.org/ontology/bibo/oclcnum', Content: '767764071'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-11/item/BV039685251'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-12/item/BV039685251'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-188/item/BV039685251'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-19/item/BV039685251'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-20/item/BV039685251'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-355/item/BV039685251'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-384/item/BV039685251'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-473/item/BV039685251'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-70/item/BV039685251'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-824/item/BV039685251'",
            u"We ignore the following information: 'http://rdvocab.info/Elements/otherTitleInformation', Content: '4: \x98Abt. IV\x9c Gedanken und Erinnerungen'",
            u"We ignore the following information: 'http://rdvocab.info/Elements/publicationStatement', Content: 'Paderborn ; M\xfcnchen [u.a.] : Sch\xf6ningh 2012'",
            u"We ignore the following information: 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', Content: 'http://purl.org/ontology/bibo/Book'",
            u"We ignore the following information: 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', Content: 'http://purl.org/ontology/bibo/Document'",
            u"We ignore the following information: 'http://www.w3.org/2002/07/owl#sameAs', Content: 'http://hub.culturegraph.org/about/BSZ-352472782'",
            u"We ignore the following information: 'http://www.w3.org/2002/07/owl#sameAs', Content: 'http://lod.b3kat.de/title/BV017995925/vol/4'",
            u"We ignore the following information: 'http://id.loc.gov/vocabulary/relators/aut', Content: 'http://d-nb.info/gnd/11851136X'",
        ])

        from recensio.policy.sparqlsearch import getMetadata
        metadata = getMetadata('9783506770707')
        errors = sorted([x.msg % x.args for x in self.handler.records])

        self.assertEquals(expected, metadata)
        self.assertEquals(ignored, errors)

    def testGetMetadata11(self):
        expected = {
            'bv': u'BV021824202',
            'authors': [{'firstname': u'Horst', 'lastname': u'Brettner-Messler'},
                   {'firstname': u'Stefan', 'lastname': u'Malf\xe8r'},
                {'firstname': u'Waltraud', 'lastname': u'Heindl-Langer'}],

            'ddcSubject': [],
            'isbn': u'3209054649',
            'keywords': [],
            'language': u'German',
            'location': u'Wien',
            'pages': u'361',
            'publisher': u'\xd6sterr. Bundesverl. f\xfcr Unterricht Wiss. und Kunst',
            'series': None,
            'seriesVol': None,
            'subtitle': None,
            'title': u'\x98Die\x9c Ministerratsprotokolle \xd6sterreichs und der \xd6sterreichisch-Ungarischen Monarchie 1848 - 1918',
            'year': u'2006',
        }

        ignored = sorted([
            u"We ignore the following information: 'http://id.loc.gov/vocabulary/relators/aut', Content: 'http://d-nb.info/gnd/2029391-4'",
            u"We ignore the following information: 'http://id.loc.gov/vocabulary/relators/ctb', Content: 'http://d-nb.info/gnd/109427793'",
            u"We ignore the following information: 'http://id.loc.gov/vocabulary/relators/ctb', Content: 'http://d-nb.info/gnd/123089980'",
            u"We ignore the following information: 'http://id.loc.gov/vocabulary/relators/ctb', Content: 'http://d-nb.info/gnd/151718121'",
            u"We ignore the following information: 'http://iflastandards.info/ns/isbd/elements/P1053', Content: 'XLII, 361 S.'",
            u"We ignore the following information: 'http://purl.org/dc/terms/description', Content: 'bearb und eingel von Thomas Klete\u010dka'",
            u"We ignore the following information: 'http://purl.org/dc/terms/isPartOf', Content: 'http://lod.b3kat.de/title/BV000497061'",
            u"We ignore the following information: 'http://purl.org/ontology/bibo/oclcnum', Content: '162254391'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-12/item/BV021824202'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-19/item/BV021824202'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-384/item/BV021824202'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-706/item/BV021824202'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-739/item/BV021824202'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-824/item/BV021824202'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-M333/item/BV021824202'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-M457/item/BV021824202'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-Re13/item/BV021824202'",
            u"We ignore the following information: 'http://rdvocab.info/Elements/otherTitleInformation', Content: '123: \x98Die\x9c Protokolle des \xd6sterreichischen Ministerrates 1848 - 1867 ; 2 Das Ministerium Schwarzenberg ; 3 1. Mai 1850 - 30. September 1850'",
            u"We ignore the following information: 'http://rdvocab.info/Elements/publicationStatement', Content: 'Wien : \xd6sterr. Bundesverl. f\xfcr Unterricht Wiss. und Kunst 2006'",
            u"We ignore the following information: 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', Content: 'http://purl.org/ontology/bibo/Book'",
            u"We ignore the following information: 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', Content: 'http://purl.org/ontology/bibo/Document'",
            u"We ignore the following information: 'http://www.w3.org/2002/07/owl#sameAs', Content: 'http://hub.culturegraph.org/about/BVB-BV021824202'",
            u"We ignore the following information: 'http://www.w3.org/2002/07/owl#sameAs', Content: 'http://lod.b3kat.de/title/BV000497061/vol/123'",
            u"We ignore the following information: 'http://id.loc.gov/vocabulary/relators/aut', Content: 'http://d-nb.info/gnd/2019327-0'",
        ])

        from recensio.policy.sparqlsearch import getMetadata
        metadata = getMetadata('3209054649')
        errors = sorted([x.msg % x.args for x in self.handler.records])

        self.assertEquals(expected, metadata)
        #self.assertEquals(ignored, errors)

    def testGetMetadata14(self):
        expected = {
            'bv': u'BV039643545',
            'authors': [
                {'firstname': u'David', 'lastname': u'Cannadine'},
                {'firstname': u'Jenny', 'lastname': u'Keating'},
                {'firstname': u'Nicola', 'lastname': u'Sheldon'},
            ],
            'ddcSubject': [u'370.9', u'901'],
            'ddcPlace': [u'41'],
            'ddcTime': [u'0904'],
            'isbn': u'9780230300873',
            'keywords': [u'England', u'Geschichte 1900-2010', u'Geschichtsunterricht'],
            'language': u'English',
            'location': u'Basingstoke',
            'pages': u'306',
            'publisher': u'Palgrave Macmillan',
            'series': None,
            'seriesVol': None,
            'subtitle': u'teaching the past in twentieth century England',
            'title': u'\x98The\x9c right kind of history',
            'year': u'2011',
        }

        ignored = sorted([
            u"We ignore the following information: 'http://id.loc.gov/vocabulary/relators/aut', Content: 'http://d-nb.info/gnd/129956481'",
            u"We ignore the following information: 'http://id.loc.gov/vocabulary/relators/aut', Content: 'http://d-nb.info/gnd/137022662'",
            u"We ignore the following information: 'http://iflastandards.info/ns/isbd/elements/P1053', Content: 'XIII, 306 S. Ill.'",
            u"We ignore the following information: 'http://purl.org/dc/terms/description', Content: 'David Cannadine ; Jenny Keating ; Nicola Sheldon'",
            u"We ignore the following information: 'http://purl.org/ontology/bibo/edition', Content: '1. publ.'",
            u"We ignore the following information: 'http://purl.org/ontology/bibo/oclcnum', Content: '713185358'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-12/item/BV039643545'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-29/item/BV039643545'",
            u"We ignore the following information: 'http://rdvocab.info/Elements/otherTitleInformation', Content: 'teaching the past in twentieth century England'",
            u"We ignore the following information: 'http://rdvocab.info/Elements/publicationStatement', Content: 'Basingstoke : Palgrave Macmillan 2011'",
            u"We ignore the following information: 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', Content: 'http://purl.org/ontology/bibo/Book'",
            u"We ignore the following information: 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', Content: 'http://purl.org/ontology/bibo/Document'",
            u"We ignore the following information: 'http://www.w3.org/2002/07/owl#sameAs', Content: 'http://hub.culturegraph.org/about/BVB-BV039643545'",
            u"We ignore the following information: 'http://id.loc.gov/vocabulary/relators/aut', Content: 'http://d-nb.info/gnd/101622740X'",
        ])
        from recensio.policy.sparqlsearch import getMetadata
        metadata = getMetadata('9780230300866')
        errors = sorted([x.msg % x.args for x in self.handler.records])

        self.assertEquals(expected, metadata)
        self.assertEquals(ignored, errors)

    def testGetMetadata16(self):
        expected = {
            'bv': u'BV036741017',
            'authors': [{'firstname': u'Vladim\xedr', 'lastname': u'Macura'}],
            'ddcSubject': [],
            'isbn': u'9780299248949',
            'keywords': [],
            'language': u'English',
            'location': u'Madison Wis.',
            'pages': u'139',
            'publisher': u'Univ. of Wisconsin Press',
            'series': None,
            'seriesVol': None,
            'subtitle': u'the Potato bug and other essays on Czech culture',
            'title': u'\x98The\x9c mystifications of a nation',
            'year': u'2010',
        }

        ignored = sorted([
            u"We ignore the following information: 'http://iflastandards.info/ns/isbd/elements/P1053', Content: 'XXVI, 139 S. Ill.'",
            u"We ignore the following information: 'http://purl.org/dc/terms/description', Content: 'Vladim\xedr Macura'",
            u"We ignore the following information: 'http://purl.org/ontology/bibo/oclcnum', Content: '711801203'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-11/item/BV036741017'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-12/item/BV036741017'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-M457/item/BV036741017'",
            u"We ignore the following information: 'http://rdvocab.info/Elements/otherTitleInformation', Content: 'the Potato bug and other essays on Czech culture'",
            u"We ignore the following information: 'http://rdvocab.info/Elements/publicationStatement', Content: 'Madison Wis. : Univ. of Wisconsin Press 2010'",
            u"We ignore the following information: 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', Content: 'http://purl.org/ontology/bibo/Book'",
            u"We ignore the following information: 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', Content: 'http://purl.org/ontology/bibo/Document'",
            u"We ignore the following information: 'http://www.w3.org/2002/07/owl#sameAs', Content: 'http://hub.culturegraph.org/about/BVB-BV036741017'",
            u"We ignore the following information: 'http://id.loc.gov/vocabulary/relators/aut', Content: 'http://d-nb.info/gnd/122514378'",
        ])

        from recensio.policy.sparqlsearch import getMetadata
        metadata = getMetadata('9780299248949')
        errors = sorted([x.msg % x.args for x in self.handler.records])

        self.assertEquals(expected, metadata)
        self.assertEquals(ignored, errors)

    def testGetMetadata17(self):
        expected = {
            'bv': u'BV035905206',
            'authors': [{'firstname': u'Wac\u0142aw', 'lastname': u'Dubia\u0144ski'}],
            'ddcSubject': [u'909'],
            'ddcPlace': [u'438'],
            'ddcTime': [u'0904'],
            'isbn': u'9788361458258',
            'keywords': [
                u'Biographie',
                u'Geschichte 1945-1990',
                u'Mitarbeiter',
                u'Staatsschutz',
                u'Woiwodschaft Bielitz-Biala',
                u'Woiwodschaft Cz\u0119stochowa',
                u'Woiwodschaft Kattowitz',
            ],
            'language': u'Polish',
            'location': u'Katowice',
            'pages': u'552',
            'publisher': u'Oddzia\u0142 Instytutu Pami\u0119ci Narodowej - Komisji \u015acigania Zbrodni przeciwko Narodowi Polskiemu',
            'series': None,
            'seriesVol': None,
            'subtitle': u'obsada stanowisk kierowniczych aparatu bezpiecze\u0144stwa w wojew\xf3dztwach \u015bl\u0105skim/katowickim, bielskim i cz\u0119stochowskim',
            'title': u'Kadra bezpieki 1945 - 1990',
            'year': u'2009',
        }

        ignored = sorted([
            u"We ignore the following information: 'http://id.loc.gov/vocabulary/relators/ctb', Content: 'http://d-nb.info/gnd/139560939'",
            u"We ignore the following information: 'http://iflastandards.info/ns/isbd/elements/P1053', Content: '552 S. Ill., graph. Darst.'",
            u"We ignore the following information: 'http://purl.org/dc/terms/description', Content: 'wst\u0119p i red Wac\u0142aw Dubia\u0144ski, Adam Dziuba i Adam Dziurok ; oprac Kornelia Bana\u015b [et al]'",
            u"We ignore the following information: 'http://purl.org/ontology/bibo/oclcnum', Content: '643765360'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-12/item/BV035905206'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-M352/item/BV035905206'",
            u"We ignore the following information: 'http://rdvocab.info/Elements/otherTitleInformation', Content: 'obsada stanowisk kierowniczych aparatu bezpiecze\u0144stwa w wojew\xf3dztwach \u015bl\u0105skim/katowickim, bielskim i cz\u0119stochowskim'",
            u"We ignore the following information: 'http://rdvocab.info/Elements/publicationStatement', Content: 'Katowice : Oddzia\u0142 Instytutu Pami\u0119ci Narodowej - Komisji \u015acigania Zbrodni przeciwko Narodowi Polskiemu 2009'",
            u"We ignore the following information: 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', Content: 'http://purl.org/ontology/bibo/Book'",
            u"We ignore the following information: 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', Content: 'http://purl.org/ontology/bibo/Document'",
            u"We ignore the following information: 'http://www.w3.org/2002/07/owl#sameAs', Content: 'http://hub.culturegraph.org/about/BVB-BV035905206'",
        ])
        from recensio.policy.sparqlsearch import getMetadata
        metadata = getMetadata('9788361458258')
        errors = sorted([x.msg % x.args for x in self.handler.records])

        self.assertEquals(expected, metadata)
        self.assertEquals(ignored, errors)

    def testGetMetadata18(self):
        expected = {
            'bv': u'BV037483285',
            'authors': [{'firstname': u'Jacek', 'lastname': u'Gzella'}],
            'ddcSubject': [u'909'],
            'ddcPlace': [u'438'],
            'ddcTime': [u'0904'],
            'isbn': u'9788323126270',
            'keywords': [u'Au\xdfenpolitik',
                         u'Deutschland',
                         u'Geschichte 1922-1939',
                         u'Polen',
                         u'Sowjetunion'],
            'language': u'Polish',
            'location': u'Toru\u0144',
            'pages': u'477',
            'publisher': u'Wydawn. Naukowe Uniwersytetu Miko\u0142aja Kopernika',
            'series': None,
            'seriesVol': None,
            'subtitle': u'koncepcje polskiej polityki zagranicznej konserwatyst\xf3w wile\u0144skich zgrupowanych wok\xf3\u0142 "S\u0142owa" (1922 - 1939)',
            'title': u'Mi\u0119dzy Sowietami a Niemcami',
            'year': u'2011'}

        ignored = sorted([
            u"We ignore the following information: 'http://id.loc.gov/vocabulary/relators/aut', Content: 'http://d-nb.info/gnd/103670823'",
            u"We ignore the following information: 'http://iflastandards.info/ns/isbd/elements/P1053', Content: '477 S.'",
            u"We ignore the following information: 'http://purl.org/dc/terms/description', Content: 'Jacek Gzella'",
            u"We ignore the following information: 'http://purl.org/dc/terms/description', Content: 'Zsfassung in dt Sprache udT: Zwischen Sowjets und Deutschen'",
            u"We ignore the following information: 'http://purl.org/ontology/bibo/edition', Content: 'Wyd. 1.'",
            u"We ignore the following information: 'http://purl.org/ontology/bibo/oclcnum', Content: '734083964'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-11/item/BV037483285'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-12/item/BV037483285'",
            u"We ignore the following information: 'http://rdvocab.info/Elements/publicationStatement', Content: 'Toru\u0144 : Wydawn. Naukowe Uniwersytetu Miko\u0142aja Kopernika 2011'",
            u"We ignore the following information: 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', Content: 'http://purl.org/ontology/bibo/Book'",
            u"We ignore the following information: 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', Content: 'http://purl.org/ontology/bibo/Document'",
            u"We ignore the following information: 'http://www.w3.org/2002/07/owl#sameAs', Content: 'http://hub.culturegraph.org/about/BVB-BV037483285'",
            u'We ignore the following information: \'http://rdvocab.info/Elements/otherTitleInformation\', Content: \'koncepcje polskiej polityki zagranicznej konserwatyst\xf3w wile\u0144skich zgrupowanych wok\xf3\u0142 "S\u0142owa" (1922 - 1939)\'',
        ])

        from recensio.policy.sparqlsearch import getMetadata
        metadata = getMetadata('9788323126270')
        errors = sorted([x.msg % x.args for x in self.handler.records])
        self.assertEquals(expected, metadata)
        self.assertEquals(ignored, errors)

    def testGetMetadata19(self):
        expected = {
            'bv': None,
            'authors': [],
            'ddcSubject': [],
            'isbn': None,
            'keywords': [],
            'language': None,
            'location': None,
            'pages': None,
            'publisher': None,
            'series': None,
            'seriesVol': None,
            'subtitle': None,
            'title': None,
            'year': None,
        }

        ignored = sorted([])

        from recensio.policy.sparqlsearch import getMetadata
        metadata = getMetadata('00157902')
        errors = sorted([x.msg % x.args for x in self.handler.records])

        self.assertEquals(expected, metadata)
        self.assertEquals(ignored, errors)



    def testGetIgnoredMetadata01(self):
        from recensio.policy.sparqlsearch import getMetadata

        result = getMetadata('9783830921929')
        errors = sorted([x.msg % x.args for x in self.handler.records])

        ignored = sorted([
            u"We ignore the following information: 'http://purl.org/dc/terms/description', Content: 'Literaturangaben'",
            u"We ignore the following information: 'http://purl.org/dc/terms/description', Content: '[Ministerium f\xfcr Generationen, Familie, Frauen und Integration des Landes Nordrhein-Westfalen, Referat \xd6ffentlichkeitsarbeit]'",
            u"We ignore the following information: 'http://purl.org/ontology/bibo/oclcnum', Content: '458749769'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-11/item/BV035724519'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-12/item/BV035724519'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-19/item/BV035724519'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-20/item/BV035724519'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-355/item/BV035724519'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-824/item/BV035724519'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-B1533/item/BV035724519'",
            u"We ignore the following information: 'http://rdvocab.info/Elements/publicationStatement', Content: 'M\xfcnster ; New York NY ; M\xfcnchen ; Berlin : Waxmann 2009'",
            u"We ignore the following information: 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', Content: 'http://purl.org/ontology/bibo/Book'",
            u"We ignore the following information: 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', Content: 'http://purl.org/ontology/bibo/Document'",
            u"We ignore the following information: 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', Content: 'http://purl.org/ontology/bibo/Proceedings'",
            u"We ignore the following information: 'http://www.w3.org/2002/07/owl#sameAs', Content: 'http://hub.culturegraph.org/about/DNB-996521429'",
            u'We ignore the following information: \'http://rdvocab.info/Elements/otherTitleInformation\', Content: \'Sprachentwicklung und Sprachf\xf6rderung in Kindertagesst\xe4tten ; [anl\xe4sslich des Landeskongresses "Kinder Bilden Sprache - Sprache Bildet Kinder" am 4. November 2008 in Recklinghausen]\'',
            "We ignore the following information: 'http://iflastandards.info/ns/isbd/elements/P1053', Content: '162 S. Ill., Noten 24 cm'",
        ])
        self.assertEquals(ignored, errors)


    def testIgnoredMetadata02(self):
        from recensio.policy.sparqlsearch import getMetadata
        metadata = getMetadata('978-0-19-928007-0')

        #Don't know how to handle http://purl.org/ontology/bibo/lccn. Contents: DD237",
        ignored = sorted([
            u"We ignore the following information: 'http://id.loc.gov/vocabulary/relators/ctb', Content: 'http://d-nb.info/gnd/122021983'",
            u"We ignore the following information: 'http://id.loc.gov/vocabulary/relators/ctb', Content: 'http://d-nb.info/gnd/122021983'",
            u"We ignore the following information: 'http://iflastandards.info/ns/isbd/elements/P1053', Content: 'XVIII, 324 S.'",
            u"We ignore the following information: 'http://iflastandards.info/ns/isbd/elements/P1053', Content: 'XVIII, 324 S.'",
            u"We ignore the following information: 'http://purl.org/dc/terms/description', Content: 'Includes bibliographical references and index'",
            u"We ignore the following information: 'http://purl.org/dc/terms/description', Content: 'Includes bibliographical references and index'",
            u"We ignore the following information: 'http://purl.org/dc/terms/description', Content: 'ed by Anthony McElligott'",
            u"We ignore the following information: 'http://purl.org/dc/terms/description', Content: 'ed by Anthony McElligott'",
            u"We ignore the following information: 'http://purl.org/ontology/bibo/edition', Content: '1. publ.'",
            u"We ignore the following information: 'http://purl.org/ontology/bibo/edition', Content: 'Repr.'",
            u"We ignore the following information: 'http://purl.org/ontology/bibo/oclcnum', Content: '276335888'",
            u"We ignore the following information: 'http://purl.org/ontology/bibo/oclcnum', Content: '694875648'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-11/item/BV036604193'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-12/item/BV035356471'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-188/item/BV035356471'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-19/item/BV035356471'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-355/item/BV035356471'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-384/item/BV035356471'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-706/item/BV036604193'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-739/item/BV036604193'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-824/item/BV035356471'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-M352/item/BV035356471'",
            u"We ignore the following information: 'http://rdvocab.info/Elements/publicationStatement', Content: 'Oxford [u.a.] : Oxford Univ. Press 2009'",
            u"We ignore the following information: 'http://rdvocab.info/Elements/publicationStatement', Content: 'Oxford [u.a.] : Oxford Univ. Press 2010'",
            u"We ignore the following information: 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', Content: 'http://purl.org/ontology/bibo/Book'",
            u"We ignore the following information: 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', Content: 'http://purl.org/ontology/bibo/Book'",
            u"We ignore the following information: 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', Content: 'http://purl.org/ontology/bibo/Document'",
            u"We ignore the following information: 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', Content: 'http://purl.org/ontology/bibo/Document'",
            u"We ignore the following information: 'http://www.w3.org/2002/07/owl#sameAs', Content: 'http://hub.culturegraph.org/about/BVB-BV035356471'",
            u"We ignore the following information: 'http://www.w3.org/2002/07/owl#sameAs', Content: 'http://hub.culturegraph.org/about/BVB-BV036604193'",
        ])

        errors = sorted([x.msg % x.args for x in self.handler.records])
        self.assertEquals(ignored, errors)

    def testGetIgnoredMetadata03(self):
        from recensio.policy.sparqlsearch import getMetadata
        metadata = getMetadata('9783898617277')

        # u"Don't know how to handle http://id.loc.gov/vocabulary/relators/edt. Contents: http://d-nb.info/gnd/111006023",
        # u"Don't know how to handle http://purl.org/ontology/bibo/lccn. Contents: D522.42",
        ignored = sorted([
            u"We ignore the following information: 'http://id.loc.gov/vocabulary/relators/ctb', Content: 'http://d-nb.info/gnd/129683922'",
            u"We ignore the following information: 'http://iflastandards.info/ns/isbd/elements/P1053', Content: '222 S. Ill.'",
            u"We ignore the following information: 'http://iflastandards.info/ns/isbd/elements/P1053', Content: '222 S.'",
            u"We ignore the following information: 'http://purl.org/dc/terms/description', Content: 'hrsg von Barbara Korte'",
            u"We ignore the following information: 'http://purl.org/dc/terms/description', Content: 'hrsg von Barbara Korte'",
            u"We ignore the following information: 'http://purl.org/dc/terms/hasPart', Content: 'http://lod.b3kat.de/title/BV023169149/vol/2746'",
            u"We ignore the following information: 'http://purl.org/dc/terms/hasPart', Content: 'http://lod.b3kat.de/title/BV023169149/vol/4757'",
            u"We ignore the following information: 'http://purl.org/dc/terms/hasPart', Content: 'http://lod.b3kat.de/title/BV023169149/vol/5971'",
            u"We ignore the following information: 'http://purl.org/dc/terms/identifier', Content: '9783898617277'",
            u"We ignore the following information: 'http://purl.org/dc/terms/isPartOf', Content: 'http://lod.b3kat.de/title/BV007921367'",
            u"We ignore the following information: 'http://purl.org/ontology/bibo/edition', Content: '1. Aufl.'",
            u"We ignore the following information: 'http://purl.org/ontology/bibo/oclcnum', Content: '244057457'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-11/item/BV023169149'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-12/item/BV023169149'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-188/item/BV023169149'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-19/item/BV023169149'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-20/item/BV023169149'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-29/item/BV023169149'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-384/item/BV023169149'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-473/item/BV023169149'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-706/item/BV023169149'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-739/item/BV023169149'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-B1550/item/BV027508403'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-B496/item/BV023169149'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-M352/item/BV023169149'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-M472/item/BV023169149'",
            u"We ignore the following information: 'http://rdvocab.info/Elements/publicationStatement', Content: 'Essen : Klartext 2008'",
            u"We ignore the following information: 'http://rdvocab.info/Elements/publicationStatement', Content: 'Essen : Klartext 2008'",
            u"We ignore the following information: 'http://www.geonames.org/ontology#countryCode', Content: 'DE'",
            u"We ignore the following information: 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', Content: 'http://purl.org/ontology/bibo/Book'",
            u"We ignore the following information: 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', Content: 'http://purl.org/ontology/bibo/Book'",
            u"We ignore the following information: 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', Content: 'http://purl.org/ontology/bibo/Document'",
            u"We ignore the following information: 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', Content: 'http://purl.org/ontology/bibo/Document'",
            u"We ignore the following information: 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', Content: 'http://xmlns.com/foaf/0.1/Document'",
            u"We ignore the following information: 'http://www.w3.org/2002/07/owl#sameAs', Content: 'http://hub.culturegraph.org/about/BVB-BV027508403'",
            u"We ignore the following information: 'http://www.w3.org/2002/07/owl#sameAs', Content: 'http://hub.culturegraph.org/about/DNB-987356151'",
            u"We ignore the following information: 'http://www.w3.org/2002/07/owl#sameAs', Content: 'http://lod.b3kat.de/title/BV007921367/vol/22'",
        ])

        errors = sorted([x.msg % x.args for x in self.handler.records])
        self.assertEquals(ignored, errors)

    # Gives unstable results for location and subtitle
    def testGetMetadata05(self):
        expected = {
            'bv': u'BV035943745',
            'authors': [{'firstname': u'Michael', 'lastname': u'Kotulla'}],
            'ddcSubject': [],
            'isbn': u'3540294961',
            'keywords': [],
            'language': u'German',
            'location': u'Germany',
            'pages': u'2081',
            'publisher': u'Springer',
            'series': None,
            'seriesVol': None,
            'subtitle': u'1806 - 1918 ; eine Dokumentensammlung nebst Einf\xfchrungen',
            'title': u'Deutsches Verfassungsrecht 1806 - 1918',
            'year': u'2010',
        }

        ignored = sorted([])

        from recensio.policy.sparqlsearch import getMetadata
        metadata = getMetadata('9783540294962')
        errors = sorted([x.msg % x.args for x in self.handler.records])

        self.assertEquals(expected, metadata)
        self.assertEquals(ignored, errors)

    def testGetMetadata07(self):
        expected = {
            'bv': u'BV023363303',
            'authors': [{'firstname': u'Volker', 'lastname': u'Stalmann'}],
            'ddcSubject': [],
            'isbn': u'9783770052882',
            'keywords': [
                u'Deutsche Demokratische Partei',
                u'Deutsche Staatspartei',
                u'Geschichte',
                u'Preu\xdfen',
                u'Quelle',
            ],
            'language': u'German',
            'location': u'D\xfcsseldorf',
            'pages': u'616',
            'publisher': u'Droste',
            'series': None,
            'seriesVol': None,
            'subtitle': u'die Sitzungsprotokolle der preu\xdfischen Landtagsfraktion der DDP und DStP ; 1919 - 1932',
            'title': u'Linksliberalismus in Preu\xdfen',
            'year': u'2009',
        }

        # u"Don't know how to handle this for keyword and ddc: http://d-nb.info/gnd/116380-2",
        #  u"Don't know how to handle this for keyword and ddc: http://d-nb.info/gnd/118094-0",
        #  u"Don't know how to handle this for keyword and ddc: http://d-nb.info/gnd/4240685-7",
        ignored = sorted([
            u"We ignore the following information: 'http://id.loc.gov/vocabulary/relators/ctb', Content: 'http://d-nb.info/gnd/123982413'",
            u"We ignore the following information: 'http://id.loc.gov/vocabulary/relators/ctb', Content: 'http://d-nb.info/gnd/123982413'",
            u"We ignore the following information: 'http://id.loc.gov/vocabulary/relators/ctb', Content: 'http://d-nb.info/gnd/123982413'",
            u"We ignore the following information: 'http://iflastandards.info/ns/isbd/elements/P1053', Content: 'CXL, 616 S. Ill.'",
            u"We ignore the following information: 'http://iflastandards.info/ns/isbd/elements/P1053', Content: 'V, S. 617 - 1307 Ill.'",
            u"We ignore the following information: 'http://purl.org/dc/terms/bibliographicCitation', Content: 'Quellen zur Geschichte des Parlamentarismus und der politischen Parteien : Dritte Reihe, Die Weimarer Republik : 11'",
            u"We ignore the following information: 'http://purl.org/dc/terms/bibliographicCitation', Content: 'Quellen zur Geschichte des Parlamentarismus und der politischen Parteien : Reihe 3, Die Weimarer Republik : 11,2'",
            u"We ignore the following information: 'http://purl.org/dc/terms/description', Content: 'eingel und bearb von Volker Stalmann'",
            u"We ignore the following information: 'http://purl.org/dc/terms/description', Content: 'eingel und bearb von Volker Stalmann'",
            u"We ignore the following information: 'http://purl.org/dc/terms/description', Content: 'eingel und bearb von Volker Stalmann'",
            u"We ignore the following information: 'http://purl.org/dc/terms/hasPart', Content: 'http://lod.b3kat.de/title/BV023363266/vol/1'",
            u"We ignore the following information: 'http://purl.org/dc/terms/hasPart', Content: 'http://lod.b3kat.de/title/BV023363266/vol/2'",
            u"We ignore the following information: 'http://purl.org/dc/terms/isPartOf', Content: 'http://lod.b3kat.de/title/BV000006150'",
            u"We ignore the following information: 'http://purl.org/dc/terms/isPartOf', Content: 'http://lod.b3kat.de/title/BV000006150'",
            u"We ignore the following information: 'http://purl.org/dc/terms/isPartOf', Content: 'http://lod.b3kat.de/title/BV023363266'",
            u"We ignore the following information: 'http://purl.org/dc/terms/isPartOf', Content: 'http://lod.b3kat.de/title/BV023363266'",
            u"We ignore the following information: 'http://purl.org/ontology/bibo/oclcnum', Content: '643316263'",
            u"We ignore the following information: 'http://purl.org/ontology/bibo/oclcnum', Content: '643316280'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-11/item/BV023363303'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-11/item/BV023363321'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-12/item/BV023363303'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-12/item/BV023363321'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-188/item/BV023363303'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-188/item/BV023363321'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-19/item/BV023363303'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-19/item/BV023363321'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-20/item/BV023363303'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-20/item/BV023363321'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-29/item/BV023363303'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-29/item/BV023363321'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-355/item/BV023363303'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-355/item/BV023363321'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-384/item/BV023363303'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-384/item/BV023363321'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-473/item/BV023363303'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-473/item/BV023363321'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-706/item/BV023363303'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-706/item/BV023363321'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-739/item/BV023363303'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-739/item/BV023363321'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-824/item/BV023363303'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-824/item/BV023363321'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-83/item/BV023363303'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-83/item/BV023363321'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-Bo133/item/BV023363303'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-Bo133/item/BV023363321'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-M352/item/BV023363303'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-M352/item/BV023363321'",
            u"We ignore the following information: 'http://rdvocab.info/Elements/otherTitleInformation', Content: '1: M\xe4rz 1919 bis Dezember 1922'",
            u"We ignore the following information: 'http://rdvocab.info/Elements/otherTitleInformation', Content: '2: Januar 1923 bis M\xe4rz 1932'",
            u"We ignore the following information: 'http://rdvocab.info/Elements/otherTitleInformation', Content: 'die Sitzungsprotokolle der preu\xdfischen Landtagsfraktion der DDP und DStP ; 1919 - 1932'",
            u"We ignore the following information: 'http://rdvocab.info/Elements/otherTitleInformation', Content: 'die Sitzungsprotokolle der preu\xdfischen Landtagsfraktion der DDP und DStP ; 1919 - 1932'",
            u"We ignore the following information: 'http://rdvocab.info/Elements/otherTitleInformation', Content: 'die Sitzungsprotokolle der preu\xdfischen Landtagsfraktion der DDP und DStP ; 1919 - 1932'",
            u"We ignore the following information: 'http://rdvocab.info/Elements/publicationStatement', Content: 'D\xfcsseldorf : Droste 2009'",
            u"We ignore the following information: 'http://rdvocab.info/Elements/publicationStatement', Content: 'D\xfcsseldorf : Droste 2009'",
            u"We ignore the following information: 'http://rdvocab.info/Elements/publicationStatement', Content: 'D\xfcsseldorf : Droste'",
            u"We ignore the following information: 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', Content: 'http://purl.org/ontology/bibo/Book'",
            u"We ignore the following information: 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', Content: 'http://purl.org/ontology/bibo/Book'",
            u"We ignore the following information: 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', Content: 'http://purl.org/ontology/bibo/Collection'",
            u"We ignore the following information: 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', Content: 'http://purl.org/ontology/bibo/Document'",
            u"We ignore the following information: 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', Content: 'http://purl.org/ontology/bibo/Document'",
            u"We ignore the following information: 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', Content: 'http://purl.org/ontology/bibo/Document'",
            u"We ignore the following information: 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', Content: 'http://purl.org/ontology/bibo/MultiVolumeBook'",
            u"We ignore the following information: 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', Content: 'http://xmlns.com/foaf/0.1/Document'",
            u"We ignore the following information: 'http://www.w3.org/2002/07/owl#sameAs', Content: 'http://hub.culturegraph.org/about/BVB-BV023363266'",
            u"We ignore the following information: 'http://www.w3.org/2002/07/owl#sameAs', Content: 'http://hub.culturegraph.org/about/BVB-BV023363303'",
            u"We ignore the following information: 'http://www.w3.org/2002/07/owl#sameAs', Content: 'http://hub.culturegraph.org/about/BVB-BV023363321'",
            u"We ignore the following information: 'http://www.w3.org/2002/07/owl#sameAs', Content: 'http://lod.b3kat.de/title/BV000006150/vol/111'",
            u"We ignore the following information: 'http://www.w3.org/2002/07/owl#sameAs', Content: 'http://lod.b3kat.de/title/BV000006150/vol/112'",
            u"We ignore the following information: 'http://www.w3.org/2002/07/owl#sameAs', Content: 'http://lod.b3kat.de/title/BV023363266/vol/1'",
            u"We ignore the following information: 'http://www.w3.org/2002/07/owl#sameAs', Content: 'http://lod.b3kat.de/title/BV023363266/vol/2'",
        ])

        from recensio.policy.sparqlsearch import getMetadata
        metadata = getMetadata('9783770052882')
        errors = sorted([x.msg % x.args for x in self.handler.records])

        self.assertEquals(expected, metadata)
        self.assertEquals(ignored, errors)

    def testGetMetadata08(self):
        expected = {
            'bv': None,
            'ddcSubject': [u'480', u'880', u'900'],
            'ddcPlace': [u'495'],
            'ddcTime': [u'09033', u'09034', u'0904'],
            'authors': [{'firstname': u'K\u014dnstantinos A.',
                         'lastname': u'D\u0113mad\u0113s'}],
            'isbn': u'9789601900780',
            'keywords': [u'Bukarest <2006>', u'Geschichte 1700-2000', u'Griechenland',
                         u'Kongress', u'Neogr\xe4zistik'],
            'language': u'Greek, Modern (1453-)',
            'location': u'Ath\u0113na',
            'pages': None,
            'publisher': u'Hell\u0113nika Grammata',
            'series': None,
            'seriesVol': None,
            'subtitle': u'praktika tu 3. Eur\u014dpa\xefku Synedriu Neoell\u0113nik\u014dn Spud\u014dn t\u0113s Eur\u014dpa\xefk\u0113s Etaireias Neoell\u0113nik\u014dn Spud\u014dn (EENS), Bucurest',
            'title': u'\x98O\x9c ell\u0113nikos kosmos anamesa epoch\u0113 tu Diaph\u014dtismu kai ston eikosto ai\u014dna',
            'year': None,
        }

        #u"Don't know how to handle http://id.loc.gov/vocabulary/relators/edt. Contents: http://d-nb.info/gnd/137593260",
        ignored = sorted([
            u"We ignore the following information: 'http://id.loc.gov/vocabulary/relators/ctb', Content: 'http://d-nb.info/gnd/137593260'",
            u"We ignore the following information: 'http://purl.org/dc/terms/alternative', Content: 'ell\u0113nikos'",
            u"We ignore the following information: 'http://purl.org/dc/terms/alternative', Content: '\x98Ho\x9c Hell\u0113nikos kosmos anamesa st\u0113n epoch\u0113 tu Diaph\u014dtismu kai ston eikosto ai\u014dna'",
            u"We ignore the following information: 'http://purl.org/dc/terms/alternative', Content: '\x98The\x9c Greek world between the Age of Enlightenment and the twentieth century'",
            u"We ignore the following information: 'http://purl.org/dc/terms/description', Content: 'Beitr teilw griech, neugriech, teilw engl, teilw ital, teilw franz - Teilw in griech Schr'",
            u"We ignore the following information: 'http://purl.org/dc/terms/description', Content: 'epimeleia: K\u014dnstantinos A D\u0113mad\u0113s'",
            u"We ignore the following information: 'http://purl.org/dc/terms/description', Content: 'epimeleia: K\u014dnstantinos A D\u0113mad\u0113s'",
            u"We ignore the following information: 'http://purl.org/dc/terms/hasPart', Content: 'http://lod.b3kat.de/title/BV026650936/vol/1'",
            u"We ignore the following information: 'http://purl.org/dc/terms/hasPart', Content: 'http://lod.b3kat.de/title/BV026650936/vol/2'",
            u"We ignore the following information: 'http://purl.org/dc/terms/hasPart', Content: 'http://lod.b3kat.de/title/BV026650936/vol/3'",
            u"We ignore the following information: 'http://purl.org/dc/terms/hasPart', Content: 'http://lod.b3kat.de/title/BV035182368/vol/1'",
            u"We ignore the following information: 'http://purl.org/dc/terms/hasPart', Content: 'http://lod.b3kat.de/title/BV035182368/vol/2'",
            u"We ignore the following information: 'http://purl.org/dc/terms/hasPart', Content: 'http://lod.b3kat.de/title/BV035182368/vol/3'",
            u"We ignore the following information: 'http://purl.org/ontology/bibo/oclcnum', Content: '644960505'",
            u"We ignore the following information: 'http://rdvocab.info/Elements/otherTitleInformation', Content: 'praktika tu 3. Eur\u014dpa\xefku Synedriu Neoell\u0113nik\u014dn Spud\u014dn t\u0113s Eur\u014dpa\xefk\u0113s Etaireias Neoell\u0113nik\u014dn Spud\u014dn (EENS), Bucurest'",
            u"We ignore the following information: 'http://rdvocab.info/Elements/otherTitleInformation', Content: 'praktika tu 3. Eur\u014dpa\xefku Synedriu Neoell\u0113nik\u014dn Spud\u014dn t\u0113s Eur\u014dpa\xefk\u0113s Etaireias Neoell\u0113nik\u014dn Spud\u014dn (EENS), Bukuresti, 2 - 4 Iuniu 2006'",
            u"We ignore the following information: 'http://rdvocab.info/Elements/publicationStatement', Content: 'Ath\u0113na : Ell\u0113nika Grammata'",
            u"We ignore the following information: 'http://rdvocab.info/Elements/publicationStatement', Content: 'Ath\u0113na : Hell\u0113nika Grammata'",
            u"We ignore the following information: 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', Content: 'http://purl.org/ontology/bibo/Collection'",
            u"We ignore the following information: 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', Content: 'http://purl.org/ontology/bibo/Collection'",
            u"We ignore the following information: 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', Content: 'http://purl.org/ontology/bibo/Document'",
            u"We ignore the following information: 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', Content: 'http://purl.org/ontology/bibo/Document'",
            u"We ignore the following information: 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', Content: 'http://purl.org/ontology/bibo/MultiVolumeBook'",
            u"We ignore the following information: 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', Content: 'http://purl.org/ontology/bibo/MultiVolumeBook'",
            u"We ignore the following information: 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', Content: 'http://purl.org/ontology/bibo/Proceedings'",
            u"We ignore the following information: 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', Content: 'http://purl.org/ontology/bibo/Proceedings'",
            u"We ignore the following information: 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', Content: 'http://xmlns.com/foaf/0.1/Document'",
            u"We ignore the following information: 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', Content: 'http://xmlns.com/foaf/0.1/Document'",
            u"We ignore the following information: 'http://www.w3.org/2002/07/owl#sameAs', Content: 'http://hub.culturegraph.org/about/BVB-BV026650936'",
            u"We ignore the following information: 'http://www.w3.org/2002/07/owl#sameAs', Content: 'http://hub.culturegraph.org/about/BVB-BV035182368'",
        ])

        from recensio.policy.sparqlsearch import getMetadata
        metadata = getMetadata('9789601900780')
        errors = sorted([x.msg % x.args for x in self.handler.records])

        # metadata.pop('ddcSubject')  # Unstable...
        self.assertEquals(expected, metadata)
        self.assertEquals(ignored, errors)

    def testGetMetadata09(self):
        expected = {
            'bv': u'BV022409054',
            'authors': [{'firstname': u'Edward', 'lastname': u'Rymar'}],
            'ddcSubject': [u'909'],
            'ddcPlace': [u'438'],
            'ddcTime': [u'0902', u'0903'],
            'isbn': u'8387879509',
            'keywords': [
                u'Genealogie',
                u'Geschichte 900-1700',
                u'Greifen',
                u'Herzog',
                u'Kr\xf3lowie i w\u0142adcy - Polska - Pomorze Gda\u0144skie (region)',
                u'Kr\xf3lowie i w\u0142adcy - Polska - Pomorze Zachodnie (region)',
                u'Kr\xf3lowie i w\u0142adcy - Polska - genealogia',
                u'Kr\xf3lowie i w\u0142adcy - Pomorze (region)',
                u'Pommern',
            ],
            'language': u'Polish',
            'location': u'Szczecin',
            'pages': u'608',
            'publisher': u'Ksi\u0105\u017cnica Pomorska',
            'series': None,
            'seriesVol': None,
            'subtitle': None,
            'title': u'Rodow\xf3d ksi\u0105\u017c\u0105t pomorskich',
            'year': u'2005',
        }

        #u"Don't know how to handle this for keyword and ddc: http://d-nb.info/gnd/118697501",
        ignored = sorted([
            u"We ignore the following information: 'http://id.loc.gov/vocabulary/relators/aut', Content: 'http://d-nb.info/gnd/131827324'",
            u"We ignore the following information: 'http://iflastandards.info/ns/isbd/elements/P1053', Content: '608 S. zahlr. Ill.'",
            u"We ignore the following information: 'http://purl.org/dc/terms/description', Content: 'Edward Rymar'",
            u"We ignore the following information: 'http://purl.org/dc/terms/description', Content: 'Zsfassung in dt Sprache udT: Genealogie der Herzoge von Pommern'",
            u"We ignore the following information: 'http://purl.org/ontology/bibo/edition', Content: 'Wyd. 2., popr. i uzup.'",
            u"We ignore the following information: 'http://purl.org/ontology/bibo/oclcnum', Content: '69296056'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-12/item/BV022409054'",
            u"We ignore the following information: 'http://rdvocab.info/Elements/publicationStatement', Content: 'Szczecin : Ksi\u0105\u017cnica Pomorska 2005'",
            u"We ignore the following information: 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', Content: 'http://purl.org/ontology/bibo/Book'",
            u"We ignore the following information: 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', Content: 'http://purl.org/ontology/bibo/Document'",
            u"We ignore the following information: 'http://www.w3.org/2002/07/owl#sameAs', Content: 'http://hub.culturegraph.org/about/BVB-BV022409054'",
        ])
        from recensio.policy.sparqlsearch import getMetadata
        metadata = getMetadata('8387879509')
        errors = sorted([x.msg % x.args for x in self.handler.records])

        self.assertEquals(expected, metadata)
        self.assertEquals(ignored, errors)

    def testGetMetadata10(self):
        expected = {
            'bv': u'BV035589116',
            'authors': [{'firstname': u'B\xe4rbel', 'lastname': u'Holtz'}],
            'ddcSubject': [],
            'isbn': u'9783050045719',
            'keywords': [],
            'language': u'German',
            'location': u'Berlin',
            'pages': u'382',
            'publisher': u'Akad.-Verl.',
            'series': None,
            'seriesVol': None,
            'subtitle': None,
            'title': u'\x98Das\x9c preu\xdfische Kultusministerium als Staatsbeh\xf6rde und gesellschaftliche Agentur (1817 - 1934)',
            'year': u'2009',
        }

        ignored = sorted([
            u"We ignore the following information: 'http://iflastandards.info/ns/isbd/elements/P1053', Content: 'XXXI, 382 S.'",
            u"We ignore the following information: 'http://purl.org/dc/terms/bibliographicCitation', Content: '1,1'",
            u"We ignore the following information: 'http://purl.org/dc/terms/bibliographicCitation', Content: 'Acta Borussica : Neue Folge : 2. Reihe, Preu\xdfen als Kulturstaat : 1,1'",
            u"We ignore the following information: 'http://purl.org/dc/terms/description', Content: 'mit Beitr von B\xe4rbel Holtz'",
            u"We ignore the following information: 'http://purl.org/dc/terms/isPartOf', Content: 'http://lod.b3kat.de/title/BV035589104'",
            u"We ignore the following information: 'http://purl.org/dc/terms/isPartOf', Content: 'http://lod.b3kat.de/title/BV035624943'",
            u"We ignore the following information: 'http://purl.org/ontology/bibo/oclcnum', Content: '634960083'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-11/item/BV035589116'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-12/item/BV035589116'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-19/item/BV035589116'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-384/item/BV035589116'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-578/item/BV035589116'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-703/item/BV035589116'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-739/item/BV035589116'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-824/item/BV035589116'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-M352/item/BV035589116'",
            u"We ignore the following information: 'http://rdvocab.info/Elements/otherTitleInformation', Content: '11 = Abt. 1: \x98Die\x9c Beh\xf6rde und ihr h\xf6heres Personal ; 1 Darstellung'",
            u"We ignore the following information: 'http://rdvocab.info/Elements/publicationStatement', Content: 'Berlin : Akad.-Verl. 2009'",
            u"We ignore the following information: 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', Content: 'http://purl.org/ontology/bibo/Book'",
            u"We ignore the following information: 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', Content: 'http://purl.org/ontology/bibo/Document'",
            u"We ignore the following information: 'http://www.w3.org/2002/07/owl#sameAs', Content: 'http://hub.culturegraph.org/about/BVB-BV035589116'",
            u"We ignore the following information: 'http://www.w3.org/2002/07/owl#sameAs', Content: 'http://lod.b3kat.de/title/BV035589104/vol/11'",
            u"We ignore the following information: 'http://www.w3.org/2002/07/owl#sameAs', Content: 'http://lod.b3kat.de/title/BV035624943/vol/11'",
            u"We ignore the following information: 'http://id.loc.gov/vocabulary/relators/ctb', Content: 'http://d-nb.info/gnd/107305232'",
        ])

        from recensio.policy.sparqlsearch import getMetadata
        metadata = getMetadata('9783050045719')
        errors = sorted([x.msg % x.args for x in self.handler.records])

        self.assertEquals(expected, metadata)
        self.assertEquals(ignored, errors)


    def testGetMetadata12(self):
        expected = {
            'bv': u'BV035973071',
            'authors': [{'firstname': u'Ladislav Josef', 'lastname': u'Beran'}],
            'ddcSubject': [u'909'],
            'ddcPlace': [u'43', u'437'],
            'ddcTime': [u'0904'],
            'isbn': u'9788087377024',
            'keywords': [
                u'Czechoslovakia',
                u'Geschichte 1918-1938',
                u'Minderheitenpolitik',
                u'Sudetendeutsche',
                u'Sudetenland (Czech Republic)',
                u'Tschechoslowakei',
            ],
            'language': u'Czech',
            'location': u'Praha',
            'pages': u'438',
            'publisher': u'Pulchra',
            'series': None,
            'seriesVol': None,
            'subtitle': u'syst\xe9mov\xe1 anal\xfdza sudeton\u011bmeck\xe9 politiky v \u010ceskoslovensk\xe9 republice 1918 - 1938',
            'title': u'Odep\u0159en\xe1 integrace',
            'year': u'2009',
        }

        # u"Don't know how to handle http://purl.org/ontology/bibo/lccn. Contents: DB2500.S94",
        ignored = sorted([
            u"We ignore the following information: 'http://id.loc.gov/vocabulary/relators/aut', Content: 'http://d-nb.info/gnd/140332545'",
            u"We ignore the following information: 'http://iflastandards.info/ns/isbd/elements/P1053', Content: '438 S. graph. Darst.'",
            u"We ignore the following information: 'http://purl.org/dc/terms/bibliographicCitation', Content: 'Edice Testis'",
            u"We ignore the following information: 'http://purl.org/dc/terms/description', Content: 'Ladislav Josef Beran'",
            u"We ignore the following information: 'http://purl.org/dc/terms/description', Content: 'Zsfassung in dt Sprache udT: Verweigerte Integration'",
            u"We ignore the following information: 'http://purl.org/ontology/bibo/edition', Content: '1. vyd.'",
            u"We ignore the following information: 'http://purl.org/ontology/bibo/oclcnum', Content: '603386928'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-12/item/BV035973071'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-739/item/BV035973071'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-M352/item/BV035973071'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-M457/item/BV035973071'",
            u"We ignore the following information: 'http://rdvocab.info/Elements/otherTitleInformation', Content: 'syst\xe9mov\xe1 anal\xfdza sudeton\u011bmeck\xe9 politiky v \u010ceskoslovensk\xe9 republice 1918 - 1938'",
            u"We ignore the following information: 'http://rdvocab.info/Elements/publicationStatement', Content: 'Praha : Pulchra 2009'",
            u"We ignore the following information: 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', Content: 'http://purl.org/ontology/bibo/Book'",
            u"We ignore the following information: 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', Content: 'http://purl.org/ontology/bibo/Document'",
            u"We ignore the following information: 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', Content: 'http://purl.org/ontology/bibo/Thesis'",
            u"We ignore the following information: 'http://www.w3.org/2002/07/owl#sameAs', Content: 'http://hub.culturegraph.org/about/BVB-BV035973071'",
        ])
        from recensio.policy.sparqlsearch import getMetadata
        metadata = getMetadata('9788087377024')
        errors = sorted([x.msg % x.args for x in self.handler.records])

        self.assertEquals(expected, metadata)
        self.assertEquals(ignored, errors)

    def testGetMetadata13(self):
        expected = {
            'bv': u'BV023424327',
            'authors': [{'firstname': u'Helmut', 'lastname': u'Schmidt'}],
            'ddcSubject': [u'320.943', u'909'],
            'ddcPlace': [u'43'],
            'ddcTime': [u'0904'],
            'isbn': u'9783886808632',
            'keywords': [
                u'Autobiographie',
                u'Berlin',
                u'Bonn',
                u'Deutschland',
                u'Friedenssicherung',
                u'Geopolitik',
                u'Germany',
                u'Geschichte',
                u'Globalisierung',
                u'Hamburg',
                u'Politik',
                u'Politiker',
                u'Schmidt, Helmut',
                u'Volkswirt',
                u'Welt',
                u'Wirtschaftsreform',
                u'Zukunftsforschung',
            ],
            'language': u'German',
            'location': u'M\xfcnchen',
            'pages': u'350',
            'publisher': u'Siedler',
            'series': None,
            'seriesVol': None,
            'subtitle': u'eine Bilanz',
            'title': u'Au\xdfer Dienst',
            'year': u'2008',
        }

        #u"Don't know how to handle http://purl.org/ontology/bibo/lccn. Contents: JN3971.A58",
        ignored = sorted([
            u"We ignore the following information: 'http://id.loc.gov/vocabulary/relators/aut', Content: 'http://d-nb.info/gnd/118608819'",
            u"We ignore the following information: 'http://id.loc.gov/vocabulary/relators/aut', Content: 'http://d-nb.info/gnd/118608819'",
            u"We ignore the following information: 'http://id.loc.gov/vocabulary/relators/aut', Content: 'http://d-nb.info/gnd/118608819'",
            u"We ignore the following information: 'http://id.loc.gov/vocabulary/relators/aut', Content: 'http://d-nb.info/gnd/118608819'",
            u"We ignore the following information: 'http://iflastandards.info/ns/isbd/elements/P1053', Content: '350 S.'",
            u"We ignore the following information: 'http://iflastandards.info/ns/isbd/elements/P1053', Content: '350 S.'",
            u"We ignore the following information: 'http://iflastandards.info/ns/isbd/elements/P1053', Content: '350 S.'",
            u"We ignore the following information: 'http://iflastandards.info/ns/isbd/elements/P1053', Content: '350 S.'",
            u"We ignore the following information: 'http://purl.org/dc/terms/description', Content: 'Helmut Schmidt'",
            u"We ignore the following information: 'http://purl.org/dc/terms/description', Content: 'Helmut Schmidt'",
            u"We ignore the following information: 'http://purl.org/dc/terms/description', Content: 'Helmut Schmidt'",
            u"We ignore the following information: 'http://purl.org/dc/terms/description', Content: 'Helmut Schmidt'",
            u"We ignore the following information: 'http://purl.org/dc/terms/identifier', Content: '9783886808632'",
            u"We ignore the following information: 'http://purl.org/dc/terms/identifier', Content: '9783886808632'",
            u"We ignore the following information: 'http://purl.org/dc/terms/identifier', Content: '9783886808632'",
            u"We ignore the following information: 'http://purl.org/dc/terms/identifier', Content: '9783886808632'",
            u"We ignore the following information: 'http://purl.org/ontology/bibo/edition', Content: '1. Aufl.'",
            u"We ignore the following information: 'http://purl.org/ontology/bibo/edition', Content: '3. Aufl.'",
            u"We ignore the following information: 'http://purl.org/ontology/bibo/edition', Content: '4. Aufl.'",
            u"We ignore the following information: 'http://purl.org/ontology/bibo/edition', Content: '5. Aufl.'",
            u"We ignore the following information: 'http://purl.org/ontology/bibo/oclcnum', Content: '251302367'",
            u"We ignore the following information: 'http://purl.org/ontology/bibo/oclcnum', Content: '251302367'",
            u"We ignore the following information: 'http://purl.org/ontology/bibo/oclcnum', Content: '251302367'",
            u"We ignore the following information: 'http://purl.org/ontology/bibo/oclcnum', Content: '251302367'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-11/item/BV023424327'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-12/item/BV023424327'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-127/item/BV035154634'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-154/item/BV023424327'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-155/item/BV035157816'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-19/item/BV023424327'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-20/item/BV023424327'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-209/item/BV023424327'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-384/item/BV035154634'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-473/item/BV023424327'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-521/item/BV035170461'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-54/item/BV035170461'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-577/item/BV035154634'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-70/item/BV023424327'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-703/item/BV023424327'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-706/item/BV023424327'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-739/item/BV023424327'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-824/item/BV023424327'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-863/item/BV035157816'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-Bo133/item/BV023424327'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-Bo133/item/BV035170461'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-Di1/item/BV023424327'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-M352/item/BV023424327'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-Met1/item/BV035154634'",
            u"We ignore the following information: 'http://rdvocab.info/Elements/otherTitleInformation', Content: 'eine Bilanz'",
            u"We ignore the following information: 'http://rdvocab.info/Elements/otherTitleInformation', Content: 'eine Bilanz'",
            u"We ignore the following information: 'http://rdvocab.info/Elements/otherTitleInformation', Content: 'eine Bilanz'",
            u"We ignore the following information: 'http://rdvocab.info/Elements/otherTitleInformation', Content: 'eine Bilanz'",
            u"We ignore the following information: 'http://rdvocab.info/Elements/publicationStatement', Content: 'M\xfcnchen : Siedler 2008'",
            u"We ignore the following information: 'http://rdvocab.info/Elements/publicationStatement', Content: 'M\xfcnchen : Siedler 2008'",
            u"We ignore the following information: 'http://rdvocab.info/Elements/publicationStatement', Content: 'M\xfcnchen : Siedler 2008'",
            u"We ignore the following information: 'http://rdvocab.info/Elements/publicationStatement', Content: 'M\xfcnchen : Siedler 2008'",
            u"We ignore the following information: 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', Content: 'http://purl.org/ontology/bibo/Book'",
            u"We ignore the following information: 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', Content: 'http://purl.org/ontology/bibo/Book'",
            u"We ignore the following information: 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', Content: 'http://purl.org/ontology/bibo/Book'",
            u"We ignore the following information: 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', Content: 'http://purl.org/ontology/bibo/Book'",
            u"We ignore the following information: 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', Content: 'http://purl.org/ontology/bibo/Document'",
            u"We ignore the following information: 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', Content: 'http://purl.org/ontology/bibo/Document'",
            u"We ignore the following information: 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', Content: 'http://purl.org/ontology/bibo/Document'",
            u"We ignore the following information: 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', Content: 'http://purl.org/ontology/bibo/Document'",
            u"We ignore the following information: 'http://www.w3.org/2002/07/owl#sameAs', Content: 'http://hub.culturegraph.org/about/BVB-BV035154634'",
            u"We ignore the following information: 'http://www.w3.org/2002/07/owl#sameAs', Content: 'http://hub.culturegraph.org/about/BVB-BV035157816'",
            u"We ignore the following information: 'http://www.w3.org/2002/07/owl#sameAs', Content: 'http://hub.culturegraph.org/about/DNB-988528975'",
            u"We ignore the following information: 'http://www.w3.org/2002/07/owl#sameAs', Content: 'http://hub.culturegraph.org/about/HBZ-HT015723472'",
            u"We ignore the following information: 'http://www.w3.org/2002/07/owl#sameAs', Content: 'http://lobid.org/resource/HT015723472/about'",
        ])

        from recensio.policy.sparqlsearch import getMetadata
        metadata = getMetadata('9783886808632')
        errors = sorted([x.msg % x.args for x in self.handler.records])

        self.assertEquals(expected, metadata)
        self.assertEquals(ignored, errors)

