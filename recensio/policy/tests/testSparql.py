#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest2 as unittest

import logging
from zope.testing.loggingsupport import InstalledHandler


class TestSparql(unittest.TestCase):
    level = 100

    def setUp(self):
        self.handler = InstalledHandler('recensio')
        self.maxDiff = None

    def tearDown(self):
        self.handler.uninstall()

    def testGetLabels(self):
        from rdflib.graph import Graph
        from recensio.policy.sparqlsearch import getLabels
        graph = Graph()
        test_url = 'http://id.loc.gov/vocabulary/iso639-2/und'
        graph.parse(test_url)
        expected = {u'fr': u'Ind\xe9termin\xe9e',
                    u'en': u'Undetermined'}
        self.assertEquals(expected, getLabels(test_url, graph))

    def testGetEmptyMetadata(self):
        from recensio.policy.sparqlsearch import getMetadata

        # http://lod.b3kat.de/title/BV013575871

        expected = {
            'ddc': None,
            'isbn': u'123',
            'keywords': [],
            'language': u'English',
            'location': u'K\xf8benhavn',
            'pages': u'223',
            'publisher': None,
            'subtitle': None,
            'title': u'Structural studies in the Pre-Cambrian of western Greenland. 2: Geology of Tovqussap Nun\xe1',
            'year': u'1960',
        }

        is_ = getMetadata('123')
        is_.pop('authors')

        ignored = sorted([
            u"We ignore the following information: "
            u"'http://purl.org/dc/terms/isPartOf', Content: "
            u"'http://lod.b3kat.de/title/BV000898335'",
            u"We ignore the following information: "
            u"'http://purl.org/dc/terms/description', "
            u"Content: 'by Asger Berthelsen'",
            u"We ignore the following information: "
            u"'http://purl.org/dc/terms/isPartOf', Content: "
            u"'http://lod.b3kat.de/title/BV013568231'",
            u"We ignore the following information: "
            u"'http://purl.org/vocab/frbr/core#exemplar', Content: "
            u"'http://lod.b3kat.de/bib/DE-11/item/BV013575871'",
            u"We ignore the following information: "
            u"'http://purl.org/vocab/frbr/core#exemplar', Content: "
            u"'http://lod.b3kat.de/bib/DE-188/item/BV013575871'",
            u"We ignore the following information: "
            u"'http://purl.org/vocab/frbr/core#exemplar', Content: "
            u"'http://lod.b3kat.de/bib/DE-19/item/BV013575871'",
            u"We ignore the following information: "
            u"'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', Content: "
            u"'http://purl.org/ontology/bibo/Book'",
            u"We ignore the following information: "
            u"'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', Content: "
            u"'http://purl.org/ontology/bibo/Thesis'",
            u"We ignore the following information: "
            u"'http://www.w3.org/2002/07/owl#sameAs', Content: "
            u"'http://lod.b3kat.de/title/BV000898335/vol/25'",
            u"We ignore the following information: "
            u"'http://www.w3.org/2002/07/owl#sameAs', Content: "
            u"'http://lod.b3kat.de/title/BV013568231/vol/2'",
            u"We ignore the following information: "
            u"'http://xmlns.com/foaf/0.1/homepage', Content: "
            u"'http://worldcat.org/oclc/312158810'",
            u"We ignore the following information: "
            u"'http://purl.org/dc/terms/description', Content: "
            u"'SA aus: Meddelelser om Gronland ; 123,1'"
        ])

        errors = [x.msg % x.args for x in self.handler.records]
        errors.sort()

        self.assertEquals(ignored, errors)

        self.assertEquals(expected, is_)

    def testGetMetadata01(self):
        from recensio.policy.sparqlsearch import getMetadata

        # http://lod.b3kat.de/title/BV035724519

        expected = {
            'authors': [],
            'ddc': u'372.6049',
            'isbn': u'9783830921929',
            'keywords': [u'Kindertagesst\xe4tte',
                         u'Kindertagesst\xe4tte - Spracherziehung - Kongress - Recklinghausen <2008>',
                         u'Kongress',
                         u'Recklinghausen <2008>',
                         u'Spracherziehung'],
            'language': u'German',
            'location': u'M\xfcnster ; New York NY ; M\xfcnchen ; Berlin',
            'pages': u'162',
            'publisher': u'Waxmann',
            'subtitle': u'Sprachentwicklung und Sprachf\xf6rderung in Kindertagesst\xe4tten ; [anl\xe4sslich des Landeskongresses \"Kinder Bilden Sprache - Sprache Bildet Kinder\" am 4. November 2008 in Recklinghausen]',
            # XXX 'title': u'Kinder bilden Sprache - Sprache bildet Kinder :
            # Sprachentwicklung und Sprachf\xf6rderung in Kindertagesst\xe4tten
            # ; [anl\xe4sslich des Landeskongresses "Kinder Bilden Sprache -
            # Sprache Bildet Kinder" am 4. November 2008 in Recklinghausen]',
            'title': u'Kinder bilden Sprache - Sprache bildet Kinder',

            'year': u'2009',
        }

        ignored = sorted([
            u"We ignore the following information: 'http://purl.org/dc/terms/description', Content: 'Literaturangaben'",
            u"We ignore the following information: 'http://purl.org/dc/terms/description', Content: '[Ministerium f\xfcr Generationen, Familie, Frauen und Integration des Landes Nordrhein-Westfalen, Referat \xd6ffentlichkeitsarbeit]'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-11/item/BV035724519'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-12/item/BV035724519'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-19/item/BV035724519'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-20/item/BV035724519'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-355/item/BV035724519'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-824/item/BV035724519'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-B1533/item/BV035724519'",
            u"We ignore the following information: 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', Content: 'http://purl.org/ontology/bibo/Book'",
            u"We ignore the following information: 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', Content: 'http://purl.org/ontology/bibo/Proceedings'",
            u"We ignore the following information: 'http://www.w3.org/2002/07/owl#sameAs', Content: 'http://d-nb.info/996521429'",
            u"We ignore the following information: 'http://www.w3.org/2002/07/owl#sameAs', Content: 'http://www.culturegraph.org/about/DNB-996521429'",
            u"We ignore the following information: 'http://xmlns.com/foaf/0.1/homepage', Content: 'http://worldcat.org/oclc/458749769'"
        ])

        result = getMetadata('9783830921929')

        errors = [x.msg % x.args for x in self.handler.records]
        errors.sort()
        self.assertEquals(ignored, errors)
        self.assertEquals(expected, result)

    def testGetMetadata02(self):
        from recensio.policy.sparqlsearch import getMetadata
        expected = {
            'ddc': u'900',
            'isbn': u'9780199280070',
            'keywords': [u'Deutschland',
                         u'Geschichte 1918-1933'],
            'language': u'English',
            'location': u'Oxford [u.a.]',
            'pages': u'324',
            'publisher': u'Oxford Univ. Press',
            'subtitle': None,
            'title': u'Weimar Germany',
            'year': u'2010',
        }
        ignored = sorted([
            u"We ignore the following information: 'http://purl.org/dc/terms/description', Content: 'Includes bibliographical references and index'",
            u"We ignore the following information: 'http://purl.org/dc/terms/description', Content: 'Includes bibliographical references and index'",
            u"We ignore the following information: 'http://purl.org/dc/terms/description', Content: 'ed by Anthony McElligott'",
            u"We ignore the following information: 'http://purl.org/dc/terms/description', Content: 'ed by Anthony McElligott'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-11/item/BV036604193'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-12/item/BV035356471'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-188/item/BV035356471'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-19/item/BV035356471'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-355/item/BV035356471'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-384/item/BV035356471'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-739/item/BV036604193'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-824/item/BV035356471'",
            u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-M352/item/BV035356471'",
            u"We ignore the following information: 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', Content: 'http://purl.org/ontology/bibo/Book'",
            u"We ignore the following information: 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', Content: 'http://purl.org/ontology/bibo/Book'",
            u"We ignore the following information: 'http://www.w3.org/2002/07/owl#sameAs', Content: 'http://www.culturegraph.org/about/BVB-BV035356471'",
            u"We ignore the following information: 'http://www.w3.org/2002/07/owl#sameAs', Content: 'http://www.culturegraph.org/about/BVB-BV036604193'",
            u"We ignore the following information: 'http://xmlns.com/foaf/0.1/homepage', Content: 'http://worldcat.org/oclc/276335888'",
            u"We ignore the following information: 'http://xmlns.com/foaf/0.1/homepage', Content: 'http://worldcat.org/oclc/694875648'"
        ])

        metadata = getMetadata('978-0-19-928007-0')
        metadata.pop('authors')
        errors = [x.msg % x.args for x in self.handler.records]
        errors.sort()

        self.assertEquals(ignored, errors)
        self.assertEquals(expected, metadata)

    def testGetMetadata03(self):
        expected = {
            'ddc': u'355.009',
            'isbn': u'9783898617277',
            'keywords': [u'Aufsatzsammlung', u'Geschichte',
                         u'Kollektives Ged\xe4chtnis',
                         u'Weltkrieg <1914-1918>'],
            'language': u'German',
            'location': u'Essen',
            'pages': u'222',
            'publisher': u'Klartext',
            'subtitle': None,
            'title': u'\x98Der\x9c Erste Weltkrieg in der popul\xe4ren Erinnerungskultur',
            'year': u'2008',
        }
        ignored = sorted([
                         u"We ignore the following information: 'http://purl.org/dc/terms/description', Content: 'hrsg von Barbara Korte'",
                         u"We ignore the following information: 'http://purl.org/dc/terms/identifier', Content: '9783898617277'",
                         u"We ignore the following information: 'http://purl.org/dc/terms/isPartOf', Content: 'http://lod.b3kat.de/title/BV007921367'",
                         u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-12/item/BV023169149'",
                         u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-188/item/BV023169149'",
                         u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-19/item/BV023169149'",
                         u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-20/item/BV023169149'",
                         u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-29/item/BV023169149'",
                         u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-384/item/BV023169149'",
                         u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-473/item/BV023169149'",
                         u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-706/item/BV023169149'",
                         u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-739/item/BV023169149'",
                         u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-M352/item/BV023169149'",
                         u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-M472/item/BV023169149'",
                         u"We ignore the following information: 'http://www.geonames.org/ontology#countryCode', Content: 'DE'",
                         u"We ignore the following information: 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', Content: 'http://purl.org/ontology/bibo/Book'",
                         u"We ignore the following information: 'http://www.w3.org/2002/07/owl#sameAs', Content: 'http://d-nb.info/987356151'",
                         u"We ignore the following information: 'http://www.w3.org/2002/07/owl#sameAs', Content: 'http://lod.b3kat.de/title/BV007921367/vol/22'",
                         u"We ignore the following information: 'http://www.w3.org/2002/07/owl#sameAs', Content: 'http://www.culturegraph.org/about/DNB-987356151'",
                         u"We ignore the following information: 'http://xmlns.com/foaf/0.1/homepage', Content: 'http://worldcat.org/oclc/244057457'"

                         ])

        from recensio.policy.sparqlsearch import getMetadata
        metadata = getMetadata('9783898617277')
        errors = [x.msg % x.args for x in self.handler.records]
        errors.sort()
        metadata.pop('authors')
        self.assertEquals(expected, metadata)
        self.assertEquals(ignored, errors)

    def testGetMetadata04(self):
        expected = {
            'ddc': None,
            'isbn': u'9783506770707',
            'keywords': [u'Deutschland', u'Politik', u'Quelle'],
            'language': u'German',
            'location': u'Paderborn ; M\xfcnchen [u.a.]',
            'pages': u'616',
            'publisher': u'Sch\xf6ningh',
            'subtitle': None,
            'title': u'Gesammelte Werke. 4: \x98Abt. IV\x9c Gedanken und Erinnerungen',
            'year': u'2012',
        }

        ignored = sorted(
            [u"We ignore the following information: 'http://purl.org/dc/terms/description', Content: 'Otto von Bismarck Hrsg von Konrad Canis'",
             u"We ignore the following information: 'http://purl.org/dc/terms/isPartOf', Content: 'http://lod.b3kat.de/title/BV017995925'",
             u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-11/item/BV039685251'",
             u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-12/item/BV039685251'",
             u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-188/item/BV039685251'",
             u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-19/item/BV039685251'",
             u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-20/item/BV039685251'",
             u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-384/item/BV039685251'",
             u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-473/item/BV039685251'",
             u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-70/item/BV039685251'",
             u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-824/item/BV039685251'",
             u"We ignore the following information: 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', Content: 'http://purl.org/ontology/bibo/Book'",
             u"We ignore the following information: 'http://www.w3.org/2002/07/owl#sameAs', Content: 'http://lod.b3kat.de/title/BV017995925/vol/4'",
             u"We ignore the following information: 'http://www.w3.org/2002/07/owl#sameAs', Content: 'http://www.culturegraph.org/about/BSZ-352472782'",
             u"We ignore the following information: 'http://xmlns.com/foaf/0.1/homepage', Content: 'http://worldcat.org/oclc/767764071'"])

        from recensio.policy.sparqlsearch import getMetadata
        metadata = getMetadata('9783506770707')
        errors = [x.msg % x.args for x in self.handler.records]
        errors.sort()
        metadata.pop('authors')
        self.assertEquals(expected, metadata)
        self.assertEquals(ignored, errors)

    def testGetMetadata05(self):
        expected = {
            'ddc': None,
            'isbn': u'3540294961',
            'keywords': [],
            'language': u'German',
            'location': u'Berlin ; Heidelberg ; New York',
            'pages': u'2081',
            'publisher': u'Springer',
            'subtitle': u'eine Dokumentensammlung nebst Einf\xfchrungen',
#            'title': u'Deutsches Verfassungsrecht 1806 - 1918 : eine Dokumentensammlung nebst Einf\xfchrungen. 3: Berg und Braunschweig',
            'title': u'Deutsches Verfassungsrecht 1806 - 1918. 3: Berg und Braunschweig',
            'year': u'2010',
        }

        ignored = sorted(
            [u"We ignore the following information: 'http://purl.org/dc/terms/description', Content: 'Michael Kotulla'",
             u"We ignore the following information: 'http://purl.org/dc/terms/description', Content: 'Michael Kotulla'",
             u"We ignore the following information: 'http://purl.org/dc/terms/description', Content: 'Michael Kotulla'",
             u"We ignore the following information: 'http://purl.org/dc/terms/identifier', Content: '10.1007/978-3-540-29497-9'",
             u"We ignore the following information: 'http://purl.org/dc/terms/isPartOf', Content: 'http://lod.b3kat.de/title/BV019888935'",
             u"We ignore the following information: 'http://purl.org/dc/terms/isPartOf', Content: 'http://lod.b3kat.de/title/BV022360137'",
             u"We ignore the following information: 'http://purl.org/dc/terms/isPartOf', Content: 'http://lod.b3kat.de/title/BV023552539'",
             u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-11/item/BV025801664'",
             u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-1102/item/BV035980226'",
             u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-12/item/BV035943745'",
             u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-12/item/BV035980226'",
             u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-188/item/BV025801664'",
             u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-19/item/BV035943745'",
             u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-19/item/BV035980226'",
  u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-20/item/BV035980226'",
  u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-29/item/BV035980226'",
  u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-355/item/BV035943745'",
  u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-355/item/BV035980226'",
  u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-473/item/BV035980226'",
  u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-525/item/BV035980226'",
  u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-526/item/BV035980226'",
  u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-703/item/BV035943745'",
  u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-703/item/BV035980226'",
  u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-706/item/BV035980226'",
  u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-739/item/BV035943745'",
  u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-739/item/BV035980226'",
  u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-824/item/BV035943745'",
  u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-824/item/BV035980226'",
  u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-858/item/BV035980226'",
  u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-859/item/BV035980226'",
  u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-860/item/BV035980226'",
  u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-862/item/BV035980226'",
  u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-863/item/BV035980226'",
  u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-898/item/BV035980226'",
  u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-92/item/BV035980226'",
  u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-Aug4/item/BV035980226'",
  u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-B1533/item/BV035980226'",
  u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-B721/item/BV035980226'",
 u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-M347/item/BV035980226'",
 u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-M483/item/BV035980226'",
 u"We ignore the following information: 'http://www.geonames.org/ontology#countryCode', Content: 'DE'",
 u"We ignore the following information: 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', Content: 'http://purl.org/dc/dcmitype/Software'",
 u"We ignore the following information: 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', Content: 'http://purl.org/ontology/bibo/Book'",
 u"We ignore the following information: 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', Content: 'http://purl.org/ontology/bibo/Book'",
 u"We ignore the following information: 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', Content: 'http://purl.org/ontology/bibo/Book'",
 u"We ignore the following information: 'http://www.w3.org/2002/07/owl#sameAs', Content: 'http://lod.b3kat.de/title/BV019888935/vol/3'",
  u"We ignore the following information: 'http://www.w3.org/2002/07/owl#sameAs', Content: 'http://lod.b3kat.de/title/BV022360137/vol/3'",
  u"We ignore the following information: 'http://www.w3.org/2002/07/owl#sameAs', Content: 'http://lod.b3kat.de/title/BV023552539/vol/3'",
  u"We ignore the following information: 'http://www.w3.org/2002/07/owl#sameAs', Content: 'http://www.culturegraph.org/about/BVB-BV025801664'",
  u"We ignore the following information: 'http://www.w3.org/2002/07/owl#sameAs', Content: 'http://www.culturegraph.org/about/BVB-BV035943745'",
  u"We ignore the following information: 'http://www.w3.org/2002/07/owl#sameAs', Content: 'http://www.culturegraph.org/about/BVB-BV035980226'",
  u"We ignore the following information: 'http://xmlns.com/foaf/0.1/homepage', Content: 'http://dx.doi.org/10.1007/978-3-540-29497-9'",
  u"We ignore the following information: 'http://xmlns.com/foaf/0.1/homepage', Content: 'http://worldcat.org/oclc/501310806'",
  u"We ignore the following information: 'http://xmlns.com/foaf/0.1/homepage', Content: 'http://worldcat.org/oclc/643865927'"])

        from recensio.policy.sparqlsearch import getMetadata
        metadata = getMetadata('9783540294962')
        errors = [x.msg % x.args for x in self.handler.records]
        errors.sort()
        metadata.pop('authors')
        self.assertEquals(expected, metadata)
        self.assertEquals(ignored, errors)

    def testGetMetadata07(self):
        expected = {
            'ddc': None,
            'isbn': u'9783770052882',
            'keywords': [u'Geschichte', u'Quelle'],
            'language': u'German',
            'location': u'D\xfcsseldorf',
            'pages': u'616',
            'publisher': u'Droste',
            'subtitle': u'die Sitzungsprotokolle der preu\xdfischen Landtagsfraktion der DDP und DStP ; 1919 - 1932',
            'title': u'Linksliberalismus in Preu\xdfen. 2: Januar 1923 bis M\xe4rz 1932',
            'year': u'2009',
        }

        ignored = sorted(
            [u"We ignore the following information: 'http://purl.org/dc/terms/description', Content: 'eingel und bearb von Volker Stalmann'",
  u"We ignore the following information: 'http://purl.org/dc/terms/description', Content: 'eingel und bearb von Volker Stalmann'",
  u"We ignore the following information: 'http://purl.org/dc/terms/description', Content: 'eingel und bearb von Volker Stalmann'",
  u"We ignore the following information: 'http://purl.org/dc/terms/hasPart', Content: 'http://lod.b3kat.de/title/BV023363266/vol/1'",
  u"We ignore the following information: 'http://purl.org/dc/terms/hasPart', Content: 'http://lod.b3kat.de/title/BV023363266/vol/2'",
  u"We ignore the following information: 'http://purl.org/dc/terms/isPartOf', Content: 'http://lod.b3kat.de/title/BV000006150'",
  u"We ignore the following information: 'http://purl.org/dc/terms/isPartOf', Content: 'http://lod.b3kat.de/title/BV000006150'",
  u"We ignore the following information: 'http://purl.org/dc/terms/isPartOf', Content: 'http://lod.b3kat.de/title/BV023363266'",
  u"We ignore the following information: 'http://purl.org/dc/terms/isPartOf', Content: 'http://lod.b3kat.de/title/BV023363266'",
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
  u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-M352/item/BV023363303'",
  u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-M352/item/BV023363321'",
  u"We ignore the following information: 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', Content: 'http://purl.org/ontology/bibo/Book'",
  u"We ignore the following information: 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', Content: 'http://purl.org/ontology/bibo/Book'",
  u"We ignore the following information: 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', Content: 'http://purl.org/ontology/bibo/MultiVolumeBook'",
  u"We ignore the following information: 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', Content: 'http://xmlns.com/foaf/0.1/Document'",
  u"We ignore the following information: 'http://www.w3.org/2002/07/owl#sameAs', Content: 'http://lod.b3kat.de/title/BV000006150/vol/111'",
  u"We ignore the following information: 'http://www.w3.org/2002/07/owl#sameAs', Content: 'http://lod.b3kat.de/title/BV000006150/vol/112'",
  u"We ignore the following information: 'http://www.w3.org/2002/07/owl#sameAs', Content: 'http://lod.b3kat.de/title/BV023363266/vol/1'",
  u"We ignore the following information: 'http://www.w3.org/2002/07/owl#sameAs', Content: 'http://lod.b3kat.de/title/BV023363266/vol/2'",
  u"We ignore the following information: 'http://www.w3.org/2002/07/owl#sameAs', Content: 'http://www.culturegraph.org/about/BVB-BV023363266'",
  u"We ignore the following information: 'http://www.w3.org/2002/07/owl#sameAs', Content: 'http://www.culturegraph.org/about/BVB-BV023363303'",
  u"We ignore the following information: 'http://www.w3.org/2002/07/owl#sameAs', Content: 'http://www.culturegraph.org/about/BVB-BV023363321'",
  u"We ignore the following information: 'http://xmlns.com/foaf/0.1/homepage', Content: 'http://worldcat.org/oclc/643316263'",
  u"We ignore the following information: 'http://xmlns.com/foaf/0.1/homepage', Content: 'http://worldcat.org/oclc/643316280'"])

        from recensio.policy.sparqlsearch import getMetadata
        metadata = getMetadata('9783770052882')
        errors = [x.msg % x.args for x in self.handler.records]
        errors.sort()
        metadata.pop('authors')
        self.assertEquals(expected, metadata)
        self.assertEquals(ignored, errors)

    def testGetMetadata08(self):
        expected = {
#            'ddc': u'880',
            'isbn': u'9789601900780',
            'keywords': [u'Bukarest <2006>', u'Geschichte 1700-2000', u'Griechenland',
                         u'Kongress', u'Neogr\xe4zistik'],
            'language': u'Greek, Modern (1453-)',
            'location': u'Ath\u0113na',
            'pages': None,
            'publisher': u'Hell\u0113nika Grammata',
            'subtitle': u'praktika tu 3. Eur\u014dpa\xefku Synedriu Neoell\u0113nik\u014dn Spud\u014dn t\u0113s Eur\u014dpa\xefk\u0113s Etaireias Neoell\u0113nik\u014dn Spud\u014dn (EENS), Bucurest',
            'title': u'\x98O\x9c ell\u0113nikos kosmos anamesa epoch\u0113 tu Diaph\u014dtismu kai ston eikosto ai\u014dna',
            'year': None,
        }

        ignored = sorted(
            [u"We ignore the following information: 'http://purl.org/dc/terms/alternative', Content: 'elell\u0113nikos'",
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
  u"We ignore the following information: 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', Content: 'http://purl.org/ontology/bibo/MultiVolumeBook'",
  u"We ignore the following information: 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', Content: 'http://purl.org/ontology/bibo/MultiVolumeBook'",
  u"We ignore the following information: 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', Content: 'http://purl.org/ontology/bibo/Proceedings'",
  u"We ignore the following information: 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', Content: 'http://purl.org/ontology/bibo/Proceedings'",
  u"We ignore the following information: 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', Content: 'http://xmlns.com/foaf/0.1/Document'",
  u"We ignore the following information: 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', Content: 'http://xmlns.com/foaf/0.1/Document'",
  u"We ignore the following information: 'http://www.w3.org/2002/07/owl#sameAs', Content: 'http://www.culturegraph.org/about/BVB-BV026650936'",
  u"We ignore the following information: 'http://www.w3.org/2002/07/owl#sameAs', Content: 'http://www.culturegraph.org/about/BVB-BV035182368'",
  u"We ignore the following information: 'http://xmlns.com/foaf/0.1/homepage', Content: 'http://worldcat.org/oclc/644960505'"])

        from recensio.policy.sparqlsearch import getMetadata
        metadata = getMetadata('9789601900780')
        errors = [x.msg % x.args for x in self.handler.records]
        errors.sort()
        metadata.pop('authors')
        metadata.pop('ddc')  # Unstable...
        self.assertEquals(expected, metadata)
        self.assertEquals(ignored, errors)

    def testGetMetadata09(self):
        expected = {
            'ddc': u'909',
            'isbn': u'8387879509',
            'keywords': [
                u'Genealogie',
                u'Geschichte 900-1700',
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
            'subtitle': None,
            'title': u'Rodow\xf3d ksi\u0105\u017c\u0105t pomorskich',
            'year': u'2005',
        }

        ignored = sorted(
            [u"We ignore the following information: 'http://purl.org/dc/terms/description', Content: 'Edward Rymar'",
  u"We ignore the following information: 'http://purl.org/dc/terms/description', Content: 'Zsfassung in dt Sprache udT: Genealogie der Herzoge von Pommern'",
  u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-12/item/BV022409054'",
  u"We ignore the following information: 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', Content: 'http://purl.org/ontology/bibo/Book'",
  u"We ignore the following information: 'http://www.w3.org/2002/07/owl#sameAs', Content: 'http://www.culturegraph.org/about/BVB-BV022409054'",
  u"We ignore the following information: 'http://xmlns.com/foaf/0.1/homepage', Content: 'http://worldcat.org/oclc/69296056'"])

        from recensio.policy.sparqlsearch import getMetadata
        metadata = getMetadata('8387879509')
        errors = [x.msg % x.args for x in self.handler.records]
        errors.sort()
        metadata.pop('authors')
        self.assertEquals(expected, metadata)
        self.assertEquals(ignored, errors)

    def testGetMetadata10(self):
        expected = {
            'ddc': None,
            'isbn': u'9783050045719',
            'keywords': [],
            'language': u'German',
            'location': u'Berlin',
            'pages': u'382',
            'publisher': u'Akad.-Verl.',
            'subtitle': None,
            'title': u'\x98Das\x9c preu\xdfische Kultusministerium als Staatsbeh\xf6rde und gesellschaftliche Agentur (1817 - 1934). 11 = Abt. 1: \x98Die\x9c Beh\xf6rde und ihr h\xf6heres Personal ; 1 Darstellung',
            'year': u'2009',
        }

        ignored = sorted(
            [u"We ignore the following information: 'http://purl.org/dc/terms/description', Content: 'mit Beitr von B\xe4rbel Holtz'",
  u"We ignore the following information: 'http://purl.org/dc/terms/isPartOf', Content: 'http://lod.b3kat.de/title/BV035589104'",
  u"We ignore the following information: 'http://purl.org/dc/terms/isPartOf', Content: 'http://lod.b3kat.de/title/BV035624943'",
  u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-11/item/BV035589116'",
  u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-12/item/BV035589116'",
  u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-19/item/BV035589116'",
  u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-384/item/BV035589116'",
  u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-578/item/BV035589116'",
  u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-703/item/BV035589116'",
  u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-739/item/BV035589116'",
  u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-824/item/BV035589116'",
  u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-M352/item/BV035589116'",
  u"We ignore the following information: 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', Content: 'http://purl.org/ontology/bibo/Book'",
  u"We ignore the following information: 'http://www.w3.org/2002/07/owl#sameAs', Content: 'http://lod.b3kat.de/title/BV035589104/vol/11'",
  u"We ignore the following information: 'http://www.w3.org/2002/07/owl#sameAs', Content: 'http://lod.b3kat.de/title/BV035624943/vol/11'",
  u"We ignore the following information: 'http://www.w3.org/2002/07/owl#sameAs', Content: 'http://www.culturegraph.org/about/BVB-BV035589116'",
  u"We ignore the following information: 'http://xmlns.com/foaf/0.1/homepage', Content: 'http://worldcat.org/oclc/634960083'"])

        from recensio.policy.sparqlsearch import getMetadata
        metadata = getMetadata('9783050045719')
        errors = [x.msg % x.args for x in self.handler.records]
        errors.sort()
        metadata.pop('authors')
        self.assertEquals(expected, metadata)
        self.assertEquals(ignored, errors)

    def testGetMetadata11(self):
        expected = {
            'ddc': None,
            'isbn': u'3209054649',
            'keywords': [],
            'language': u'German',
            'location': u'Wien',
            'pages': u'361',
            'publisher': u'\xd6sterr. Bundesverl. f\xfcr Unterricht Wiss. und Kunst',
            'subtitle': None,
            'title': u'\x98Die\x9c Ministerratsprotokolle \xd6sterreichs und der \xd6sterreichisch-Ungarischen Monarchie 1848 - 1918. 123: \x98Die\x9c Protokolle des \xd6sterreichischen Ministerrates 1848 - 1867 ; 2 Das Ministerium Schwarzenberg ; 3 1. Mai 1850 - 30. September 1850',
            'year': u'2006',
        }

        ignored = sorted(
            [u"We ignore the following information: 'http://purl.org/dc/terms/description', Content: 'bearb und eingel von Thomas Klete\u010dka'",
  u"We ignore the following information: 'http://purl.org/dc/terms/isPartOf', Content: 'http://lod.b3kat.de/title/BV000497061'",
  u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib//item/BV021824202'",
  u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-12/item/BV021824202'",
  u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-19/item/BV021824202'",
  u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-384/item/BV021824202'",
  u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-706/item/BV021824202'",
  u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-739/item/BV021824202'",
  u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-824/item/BV021824202'",
  u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-M333/item/BV021824202'",
  u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-M457/item/BV021824202'",
  u"We ignore the following information: 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', Content: 'http://purl.org/ontology/bibo/Book'",
  u"We ignore the following information: 'http://www.w3.org/2002/07/owl#sameAs', Content: 'http://lod.b3kat.de/title/BV000497061/vol/123'",
  u"We ignore the following information: 'http://xmlns.com/foaf/0.1/homepage', Content: 'http://worldcat.org/oclc/162254391'"])

        from recensio.policy.sparqlsearch import getMetadata
        metadata = getMetadata('3209054649')
        errors = [x.msg % x.args for x in self.handler.records]
        errors.sort()
        metadata.pop('authors')
        self.assertEquals(expected, metadata)
        self.assertEquals(ignored, errors)

    def testGetMetadata12(self):
        expected = {
            'ddc': u'909',
            'isbn': u'9788087377024',
            'keywords': [u'Geschichte 1918-1938', u'Minderheitenpolitik', u'Sudetendeutsche', u'Tschechoslowakei'],
            'language': u'Czech',
            'location': u'Praha',
            'pages': u'438',
            'publisher': u'Pulchra',
            'subtitle': u'syst\xe9mov\xe1 anal\xfdza sudeton\u011bmeck\xe9 politiky v \u010ceskoslovensk\xe9 republice 1918 - 1938',
            'title': u'Odep\u0159en\xe1 integrace',
            'year': u'2009',
        }

        ignored = sorted(
            [u"We ignore the following information: 'http://purl.org/dc/terms/description', Content: 'Ladislav Josef Beran'",
  u"We ignore the following information: 'http://purl.org/dc/terms/description', Content: 'Zsfassung in dt Sprache udT: Verweigerte Integration'",
  u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-12/item/BV035973071'",
  u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-739/item/BV035973071'",
  u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-M352/item/BV035973071'",
  u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-M457/item/BV035973071'",
  u"We ignore the following information: 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', Content: 'http://purl.org/ontology/bibo/Book'",
  u"We ignore the following information: 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', Content: 'http://purl.org/ontology/bibo/Thesis'",
  u"We ignore the following information: 'http://www.w3.org/2002/07/owl#sameAs', Content: 'http://www.culturegraph.org/about/BVB-BV035973071'",
  u"We ignore the following information: 'http://xmlns.com/foaf/0.1/homepage', Content: 'http://worldcat.org/oclc/603386928'"])

        from recensio.policy.sparqlsearch import getMetadata
        metadata = getMetadata('9788087377024')
        errors = [x.msg % x.args for x in self.handler.records]
        errors.sort()
        metadata.pop('authors')
        self.assertEquals(expected, metadata)
        self.assertEquals(ignored, errors)

    def testGetMetadata13(self):
        expected = {
            'ddc': u'320.943',
            'isbn': u'9783886808632',
            'keywords': [
                u'Autobiographie',
                u'Deutschland',
                u'Friedenssicherung',
                u'Geopolitik',
                u'Geschichte',
                u'Globalisierung',
                u'Politik',
                u'Welt',
                u'Wirtschaftsreform',
                u'Zukunftsforschung',
            ],
            'language': u'German',
            'location': u'M\xfcnchen',
            'pages': u'350',
            'publisher': u'Siedler',
            'subtitle':  u'eine Bilanz',
            'title': u'Au\xdfer Dienst',
            'year': u'2008',
        }

        ignored = sorted(
            [u"We ignore the following information: 'http://purl.org/dc/terms/description', Content: 'Helmut Schmidt'",
  u"We ignore the following information: 'http://purl.org/dc/terms/description', Content: 'Helmut Schmidt'",
  u"We ignore the following information: 'http://purl.org/dc/terms/description', Content: 'Helmut Schmidt'",
  u"We ignore the following information: 'http://purl.org/dc/terms/description', Content: 'Helmut Schmidt'",
  u"We ignore the following information: 'http://purl.org/dc/terms/description', Content: 'Helmut Schmidt'",
  u"We ignore the following information: 'http://purl.org/dc/terms/description', Content: 'Helmut Schmidt'",
  u"We ignore the following information: 'http://purl.org/dc/terms/identifier', Content: '9783886808632'",
  u"We ignore the following information: 'http://purl.org/dc/terms/identifier', Content: '9783886808632'",
  u"We ignore the following information: 'http://purl.org/dc/terms/identifier', Content: '9783886808632'",
  u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-1046/item/BV035364569'",
  u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-11/item/BV023424327'",
  u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-1102/item/BV035666334'",
  u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-12/item/BV023424327'",
  u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-127/item/BV035154634'",
  u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-154/item/BV023424327'",
  u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-188/item/BV035364569'",
  u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-19/item/BV023424327'",
  u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-20/item/BV023424327'",
  u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-209/item/BV023424327'",
  u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-384/item/BV035154634'",
  u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-473/item/BV023424327'",
  u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-70/item/BV023424327'",
  u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-703/item/BV023424327'",
  u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-706/item/BV023424327'",
  u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-739/item/BV023424327'",
  u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-739/item/BV035236436'",
  u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-824/item/BV023424327'",
  u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-860/item/BV035364569'",
  u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-B721/item/BV035154634'",
  u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-Di1/item/BV023424327'",
  u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-M25/item/BV035666334'",
  u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-M352/item/BV023424327'",
  u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-M497/item/BV035666334'",
  u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-M501/item/BV035236436'",
  u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-Met1/item/BV035154634'",
  u"We ignore the following information: 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', Content: 'http://purl.org/ontology/bibo/Book'",
  u"We ignore the following information: 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', Content: 'http://purl.org/ontology/bibo/Book'",
  u"We ignore the following information: 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', Content: 'http://purl.org/ontology/bibo/Book'",
  u"We ignore the following information: 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', Content: 'http://purl.org/ontology/bibo/Book'",
  u"We ignore the following information: 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', Content: 'http://purl.org/ontology/bibo/Book'",
  u"We ignore the following information: 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', Content: 'http://purl.org/ontology/bibo/Book'",
  u"We ignore the following information: 'http://www.w3.org/2002/07/owl#sameAs', Content: 'http://d-nb.info/988528975'",
  u"We ignore the following information: 'http://www.w3.org/2002/07/owl#sameAs', Content: 'http://www.culturegraph.org/about/BSZ-302278524'",
  u"We ignore the following information: 'http://www.w3.org/2002/07/owl#sameAs', Content: 'http://www.culturegraph.org/about/BVB-BV035154634'",
  u"We ignore the following information: 'http://www.w3.org/2002/07/owl#sameAs', Content: 'http://www.culturegraph.org/about/BVB-BV035157816'",
  u"We ignore the following information: 'http://www.w3.org/2002/07/owl#sameAs', Content: 'http://www.culturegraph.org/about/BVB-BV035236436'",
  u"We ignore the following information: 'http://www.w3.org/2002/07/owl#sameAs', Content: 'http://www.culturegraph.org/about/BVB-BV035666334'",
  u"We ignore the following information: 'http://www.w3.org/2002/07/owl#sameAs', Content: 'http://www.culturegraph.org/about/DNB-988528975'",
  u"We ignore the following information: 'http://xmlns.com/foaf/0.1/homepage', Content: 'http://worldcat.org/oclc/251302367'",
  u"We ignore the following information: 'http://xmlns.com/foaf/0.1/homepage', Content: 'http://worldcat.org/oclc/251302367'",
  u"We ignore the following information: 'http://xmlns.com/foaf/0.1/homepage', Content: 'http://worldcat.org/oclc/251302367'",
  u"We ignore the following information: 'http://xmlns.com/foaf/0.1/homepage', Content: 'http://worldcat.org/oclc/251302367'",
  u"We ignore the following information: 'http://xmlns.com/foaf/0.1/homepage', Content: 'http://worldcat.org/oclc/251302367'"])

        from recensio.policy.sparqlsearch import getMetadata
        metadata = getMetadata('9783886808632')
        errors = [x.msg % x.args for x in self.handler.records]
        errors.sort()
        #metadata.pop('authors')
        self.assertEquals(expected, metadata)
        self.assertEquals(ignored, errors)

    def testGetMetadata14(self):
        expected = {
            'ddc': u'901',
            'isbn': u'9783506771674',
            'keywords': [u'Geschichte 1941-1945', u'Historiker'],
            'language': u'German',
            'location': u'Paderborn [u.a.]',
            'pages': u'403',
            'publisher': u'Sch\xf6ningh',
            'subtitle': u'deutsche Historiker an der Reichsuniversit\xe4t Posen (1941 - 1945)',
            'title': u'Utopie einer besseren Tyrannis',
            'year': u'2011',
        }

        ignored = sorted(
            [u"We ignore the following information: 'http://purl.org/dc/terms/description', Content: 'B\u0142a\u017cej Bia\u0142kowski'",
  u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-11/item/BV037330325'",
  u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-12/item/BV037330325'",
  u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-19/item/BV037330325'",
  u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-355/item/BV037330325'",
  u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-521/item/BV037330325'",
  u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-739/item/BV037330325'",
  u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-824/item/BV037330325'",
  u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-83/item/BV037330325'",
  u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-B220/item/BV037330325'",
  u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-M352/item/BV037330325'",
  u"We ignore the following information: 'http://www.geonames.org/ontology#countryCode', Content: 'DE'",
  u"We ignore the following information: 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', Content: 'http://purl.org/ontology/bibo/Book'",
  u"We ignore the following information: 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', Content: 'http://purl.org/ontology/bibo/Thesis'",
  u"We ignore the following information: 'http://www.w3.org/2002/07/owl#sameAs', Content: 'http://d-nb.info/1009008978'",
  u"We ignore the following information: 'http://www.w3.org/2002/07/owl#sameAs', Content: 'http://www.culturegraph.org/about/DNB-1009008978'",
  u"We ignore the following information: 'http://xmlns.com/foaf/0.1/homepage', Content: 'http://worldcat.org/oclc/706979236'"])

        from recensio.policy.sparqlsearch import getMetadata
        metadata = getMetadata('9783506771674')
        errors = [x.msg % x.args for x in self.handler.records]
        errors.sort()
        metadata.pop('authors')
        self.assertEquals(expected, metadata)
        self.assertEquals(ignored, errors)

    def testGetMetadata15(self):
        expected = {
            'ddc': u'370.9',
            'isbn': u'9780230300873',
            'keywords': [u'England', u'Geschichte 1900-2010', u'Geschichtsunterricht'],
            'language': u'English',
            'location': u'Basingstoke',
            'pages': u'306',
            'publisher': u'Palgrave Macmillan',
            'subtitle': u'teaching the past in twentieth-century England',
            'title': u'\x98The\x9c right kind of history',
            'year': u'2011',
        }

        ignored = sorted(
            [u"We ignore the following information: 'http://purl.org/dc/terms/description', Content: 'David Cannadine ; Jenny Keating ; Nicola Sheldon'",
  u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-12/item/BV039643545'",
  u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-29/item/BV039643545'",
  u"We ignore the following information: 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', Content: 'http://purl.org/ontology/bibo/Book'",
  u"We ignore the following information: 'http://www.w3.org/2002/07/owl#sameAs', Content: 'http://www.culturegraph.org/about/BVB-BV039643545'",
  u"We ignore the following information: 'http://xmlns.com/foaf/0.1/homepage', Content: 'http://worldcat.org/oclc/713185358'"])

        from recensio.policy.sparqlsearch import getMetadata
        metadata = getMetadata('9780230300866')
        errors = [x.msg % x.args for x in self.handler.records]
        errors.sort()
        metadata.pop('authors')
        self.assertEquals(expected, metadata)
        self.assertEquals(ignored, errors)

    def testGetMetadata16(self):
        expected = {
            'ddc': None,
            'isbn': u'9780299248949',
            'keywords': [],
            'language': u'English',
            'location': u'Madison Wis.',
            'pages': u'139',
            'publisher': u'Univ. of Wisconsin Press',
            'subtitle': u'the Potato bug and other essays on Czech culture',
            'title': u'\x98The\x9c mystifications of a nation',
            'year': u'2010',
        }

        ignored = sorted(
            [u"We ignore the following information: 'http://purl.org/dc/terms/description', Content: 'Vladim\xedr Macura'",
  u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-11/item/BV036741017'",
  u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-12/item/BV036741017'",
  u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-M457/item/BV036741017'",
  u"We ignore the following information: 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', Content: 'http://purl.org/ontology/bibo/Book'",
  u"We ignore the following information: 'http://www.w3.org/2002/07/owl#sameAs', Content: 'http://www.culturegraph.org/about/BVB-BV036741017'",
  u"We ignore the following information: 'http://xmlns.com/foaf/0.1/homepage', Content: 'http://worldcat.org/oclc/711801203'"])

        from recensio.policy.sparqlsearch import getMetadata
        metadata = getMetadata('9780299248949')
        errors = [x.msg % x.args for x in self.handler.records]
        errors.sort()
        metadata.pop('authors')
        self.assertEquals(expected, metadata)
        self.assertEquals(ignored, errors)

    def testGetMetadata17(self):
        expected = {
            'ddc': u'909',
            'isbn': u'9788361458258',
            'keywords': [
                u'Biographie',
                u'Geschichte 1945-1990',
                u'Mitarbeiter',
                u'Staatsschutz',
                u'Woiwodschaft Bielitz-Biala',
                u'Woiwodschaft Cze\u031cStochowa',
                u'Woiwodschaft Kattowitz',
            ],
            'language': u'Polish',
            'location': u'Katowice',
            'pages': None,
            'publisher': u'Oddzia\u0142 Instytutu Pami\u0119ci Narodowej - Komisji \u015acigania Zbrodni przeciwko Narodowi Polskiemu',
            'subtitle': u'obsada stanowisk kierowniczych aparatu bezpiecze\u0144stwa w wojew\xf3dztwach \u015bl\u0105skim/katowickim, bielskim i cz\u0119stochowskim',
            'title': u'Kadra bezpieki 1945 - 1990',
            'year': u'2009',
        }

        ignored = sorted(
            [u"We ignore the following information: 'http://purl.org/dc/terms/description', Content: 'wst\u0119p i red Wac\u0142aw Dubia\u0144ski, Adam Dziuba i Adam Dziurok ; oprac Kornelia Bana\u015b [et al]'",
  u"We ignore the following information: 'http://purl.org/vocab/frbr/core#exemplar', Content: 'http://lod.b3kat.de/bib/DE-12/item/BV035905206'",
  u"We ignore the following information: 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', Content: 'http://purl.org/ontology/bibo/Book'",
  u"We ignore the following information: 'http://www.w3.org/2002/07/owl#sameAs', Content: 'http://www.culturegraph.org/about/BVB-BV035905206'",
  u"We ignore the following information: 'http://xmlns.com/foaf/0.1/homepage', Content: 'http://worldcat.org/oclc/643765360'"])

        from recensio.policy.sparqlsearch import getMetadata
        metadata = getMetadata('9788361458258')
        errors = [x.msg % x.args for x in self.handler.records]
        errors.sort()
        metadata.pop('authors')
        self.assertEquals(expected, metadata)
        self.assertEquals(ignored, errors)

    def testGetMetadata18(self):
        expected = {
            'ddc': None,
            'isbn': None,
            'keywords': [],
            'language': None,
            'location': None,
            'pages': None,
            'publisher': None,
            'subtitle': None,
            'title': None,
            'year': None,
        }

        ignored = sorted([])

        from recensio.policy.sparqlsearch import getMetadata
        metadata = getMetadata('00157902')
        errors = [x.msg % x.args for x in self.handler.records]
        errors.sort()
        metadata.pop('authors')
        self.assertEquals(expected, metadata)
        self.assertEquals(ignored, errors)
