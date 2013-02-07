#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest2 as unittest

import logging
from zope.testing.loggingsupport import InstalledHandler


class TestSparql(unittest.TestCase):
    level = 100

    def setUp(self):
        self.handler = InstalledHandler('recensio')
        self.maxDiff = 2000

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

        ignored = [
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
        ]

        ignored.sort()

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
            'subtitle': None,
            #XXX 'title': u'Kinder bilden Sprache - Sprache bildet Kinder : Sprachentwicklung und Sprachf\xf6rderung in Kindertagesst\xe4tten ; [anl\xe4sslich des Landeskongresses "Kinder Bilden Sprache - Sprache Bildet Kinder" am 4. November 2008 in Recklinghausen]',
            'title': u'Kinder bilden Sprache - Sprache bildet Kinder',

            'year': u'2009',
        }

        ignored = [
            u"We ignore the following information: 'http://iflastandards.info/ns/isbd/elements/P1006', Content: 'Sprachentwicklung und Sprachf\xf6rderung in Kindertagesst\xe4tten ; [anl\xe4sslich des Landeskongresses \"Kinder Bilden Sprache - Sprache Bildet Kinder\" am 4. November 2008 in Recklinghausen]'",
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
        ]

        ignored.sort()

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
        ignored = [
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
        ]

        ignored.sort()

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
            'language': u'Undetermined',
            'location': u'Essen',
            'pages': u'222',
            'publisher': u'Klartext',
            'subtitle': None,
            'title': u'Der Erste Weltkrieg in der popul\xe4ren Erinnerungskultur',
            'year': u'2008',
        }

        from recensio.policy.sparqlsearch import getMetadata
        metadata = getMetadata('9783898617277')
        metadata.pop('authors')
        self.assertEquals(expected, metadata)
        self.assertFalse([x.getMessage() for x in self.handler.records])

    def testGetMetadata04(self):
        expected = {
            'ddc': None,
            'isbn': u'9783506770707',
            'keywords': [u'Deutschland', u'Politik', u'Quelle'],
            'language': u'Undetermined',
            'location': u'Paderborn ; M\xfcnchen [u.a.]',
            'pages': u'616',
            'publisher': u'Sch\xf6ningh',
            'subtitle': None,
            'title': u'Gesammelte Werke. 4: Abt. IV Gedanken und Erinnerungen',
            'year': u'2012',
        }

        from recensio.policy.sparqlsearch import getMetadata
        metadata = getMetadata('9783506770707')
        metadata.pop('authors')
        self.assertEquals(expected, metadata)
        self.assertFalse([x.getMessage() for x in self.handler.records])

    def testGetMetadata05(self):
        expected = {
            'ddc': None,
            'isbn': u'3540294961',
            'keywords': [],
            'language': u'Undetermined',
            'location': u'Berlin ; Heidelberg ; New York',
            'pages': u'2081',
            'publisher': u'Springer',
            'subtitle': None,
            'title': u'Deutsches Verfassungsrecht 1806 - 1918 : eine Dokumentensammlung nebst Einf\xfchrungen. 3: Berg und Braunschweig',
            'year': u'2010',
        }

        from recensio.policy.sparqlsearch import getMetadata
        metadata = getMetadata('9783540294962')
        metadata.pop('authors')
        self.assertEquals(expected, metadata)
        self.assertFalse([x.getMessage() for x in self.handler.records])

    def testGetMetadata06(self):
        expected = {
            'ddc': None,
            'isbn': u'3540294961',
            'keywords': [],
            'language': u'Undetermined',
            'location': u'Berlin ; Heidelberg ; New York',
            'pages': u'2081',
            'publisher': u'Springer',
            'subtitle': None,
            'title': u'Deutsches Verfassungsrecht 1806 - 1918 : eine Dokumentensammlung nebst Einf\xfchrungen. 3: Berg und Braunschweig',
            'year': u'2010',
        }

        from recensio.policy.sparqlsearch import getMetadata
        metadata = getMetadata('9783540294962')
        metadata.pop('authors')
        self.assertEquals(expected, metadata)
        self.assertFalse([x.getMessage() for x in self.handler.records])

    def testGetMetadata07(self):
        expected = {
            'ddc': None,
            'isbn': u'9783770052882',
            'keywords': [u'Geschichte', u'Quelle'],
            'language': u'Undetermined',
            'location': u'D\xfcsseldorf',
            'pages': u'616',
            'publisher': u'Droste',
            'subtitle': None,
            'title': u'Linksliberalismus in Preu\xdfen : die Sitzungsprotokolle der preu\xdfischen Landtagsfraktion der DDP und DStP ; 1919 - 1932. 2: Januar 1923 bis M\xe4rz 1932',
            'year': u'2009',
        }

        from recensio.policy.sparqlsearch import getMetadata
        metadata = getMetadata('9783770052882')
        metadata.pop('authors')
        self.assertEquals(expected, metadata)
        self.assertFalse([x.getMessage() for x in self.handler.records])

    def testGetMetadata08(self):
        expected = {
            'ddc': u'900',
            'isbn': u'9789601900780',
            'keywords': [u'Geschichte 1700-2000', u'Griechenland',
                         u'Kongress', u'Neogr\xe4zistik'],
            'language': u'Undetermined',
            'location': u'Ath\u0113na',
            'pages': None,
            'publisher': u'Hell\u0113nika Grammata',
            'subtitle': None,
            'title': u'O ell\u0113nikos kosmos anamesa epoch\u0113 tu Diaph\u014dtismu kai ston eikosto ai\u014dna : praktika tu 3. Eur\u014dpa\xefku Synedriu Neoell\u0113nik\u014dn Spud\u014dn t\u0113s Eur\u014dpa\xefk\u0113s Etaireias Neoell\u0113nik\u014dn Spud\u014dn (EENS), Bucurest',
            'year': None,
        }

        from recensio.policy.sparqlsearch import getMetadata
        metadata = getMetadata('9789601900780')
        metadata.pop('authors')
        self.assertEquals(expected, metadata)
        self.assertFalse([x.getMessage() for x in self.handler.records])

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
            'language': u'Undetermined',
            'location': u'Szczecin',
            'pages': u'608',
            'publisher': u'Ksi\u0105\u017cnica Pomorska',
            'subtitle': None,
            'title': u'Rodow\xf3d ksi\u0105\u017c\u0105t pomorskich',
            'year': u'2005',
        }

        from recensio.policy.sparqlsearch import getMetadata
        metadata = getMetadata('8387879509')
        metadata.pop('authors')
        self.assertEquals(expected, metadata)
        self.assertFalse([x.getMessage() for x in self.handler.records])

    def testGetMetadata10(self):
        expected = {
            'ddc': None,
            'isbn': u'9783050045719',
            'keywords': [],
            'language': u'Undetermined',
            'location': u'Berlin',
            'pages': u'382',
            'publisher': u'Akad.-Verl.',
            'subtitle': None,
            'title': u'Das preu\xdfische Kultusministerium als Staatsbeh\xf6rde und gesellschaftliche Agentur (1817 - 1934). 11 = Abt. 1: Die Beh\xf6rde und ihr h\xf6heres Personal ; 1 Darstellung',
            'year': u'2009',
        }

        from recensio.policy.sparqlsearch import getMetadata
        metadata = getMetadata('9783050045719')
        metadata.pop('authors')
        self.assertEquals(expected, metadata)
        self.assertFalse([x.getMessage() for x in self.handler.records])

    def testGetMetadata11(self):
        expected = {
            'ddc': None,
            'isbn': u'3209054649',
            'keywords': [],
            'language': u'Undetermined',
            'location': u'Wien',
            'pages': u'361',
            'publisher': u'\xd6sterr. Bundesverl. f\xfcr Unterricht Wiss. und Kunst',
            'subtitle': None,
            'title': u'Die Ministerratsprotokolle \xd6sterreichs und der \xd6sterreichisch-Ungarischen Monarchie : 1848 - 1918. 123: Die Protokolle des \xd6sterreichischen Ministerrates 1848 - 1867 ; 2 Das Ministerium Schwarzenberg ; 3 1. Mai 1850 - 30. September 1850',
            'year': u'2006',
        }

        from recensio.policy.sparqlsearch import getMetadata
        metadata = getMetadata('3209054649')
        metadata.pop('authors')
        self.assertEquals(expected, metadata)
        self.assertFalse([x.getMessage() for x in self.handler.records])

    def testGetMetadata12(self):
        expected = {
            'ddc': u'909',
            'isbn': u'9788087377024',
            'keywords': [u'Geschichte 1918-1938', u'Minderheitenpolitik', u'Sudetendeutsche', u'Tschechoslowakei'],
            'language': u'Undetermined',
            'location': u'Praha',
            'pages': u'438',
            'publisher': u'Pulchra',
            'subtitle': None,
            'title': u'Odep\u0159en\xe1 integrace : syst\xe9mov\xe1 anal\xfdza sudeton\u011bmeck\xe9 politiky v \u010ceskoslovensk\xe9 republice 1918 - 1938',
            'year': u'2009',
        }

        from recensio.policy.sparqlsearch import getMetadata
        metadata = getMetadata('9788087377024')
        metadata.pop('authors')
        self.assertEquals(expected, metadata)
        self.assertFalse([x.getMessage() for x in self.handler.records])

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
            'language': u'Undetermined',
            'location': u'M\xfcnchen',
            'pages': u'350',
            'publisher': u'Siedler',
            'subtitle': None,
            'title': u'Au\xdfer Dienst : eine Bilanz',
            'year': u'2008',
        }

        from recensio.policy.sparqlsearch import getMetadata
        metadata = getMetadata('9783886808632')
        metadata.pop('authors')
        self.assertEquals(expected, metadata)
        self.assertFalse([x.getMessage() for x in self.handler.records])

    def testGetMetadata14(self):
        expected = {
            'ddc': u'901',
            'isbn': u'9783506771674',
            'keywords': [u'Geschichte 1941-1945', u'Historiker'],
            'language': u'Undetermined',
            'location': u'Paderborn ; M\xfcnchen ; Wien ; Z\xfcrich',
            'pages': u'403',
            'publisher': u'Sch\xf6ningh',
            'subtitle': None,
            'title': u'Utopie einer besseren Tyrannis : deutsche Historiker an der Reichsuniversit\xe4t Posen (1941 - 1945)',
            'year': u'2011',
        }

        from recensio.policy.sparqlsearch import getMetadata
        metadata = getMetadata('9783506771674')
        metadata.pop('authors')
        self.assertEquals(expected, metadata)
        self.assertFalse([x.getMessage() for x in self.handler.records])

    def testGetMetadata15(self):
        expected = {
            'ddc': None,
            'isbn': u'9780230300866',
            'keywords': [],
            'language': u'Undetermined',
            'location': u'Basingstoke',
            'pages': None,
            'publisher': u'Palgrave Macmillan',
            'subtitle': None,
            'title': u'The right kind of history : teaching the past in twentieth-century England',
            'year': u'2011',
        }

        from recensio.policy.sparqlsearch import getMetadata
        metadata = getMetadata('9780230300866')
        metadata.pop('authors')
        self.assertEquals(expected, metadata)
        self.assertFalse([x.getMessage() for x in self.handler.records])

    def testGetMetadata16(self):
        expected = {
            'ddc': None,
            'isbn': u'9780299248949',
            'keywords': [],
            'language': u'Undetermined',
            'location': u'Madison Wis.',
            'pages': u'139',
            'publisher': u'Univ. of Wisconsin Press',
            'subtitle': None,
            'title': u'The mystifications of a nation : the Potato bug and other essays on Czech culture',
            'year': u'2010',
        }

        from recensio.policy.sparqlsearch import getMetadata
        metadata = getMetadata('9780299248949')
        metadata.pop('authors')
        self.assertEquals(expected, metadata)
        self.assertFalse([x.getMessage() for x in self.handler.records])

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
            'language': u'Undetermined',
            'location': u'Katowice',
            'pages': None,
            'publisher': u'Oddzia\u0142 Instytutu Pami\u0119ci Narodowej - Komisji \u015acigania Zbrodni przeciwko Narodowi Polskiemu',
            'subtitle': None,
            'title': u'Kadra bezpieki 1945 - 1990 : obsada stanowisk kierowniczych aparatu bezpiecze\u0144stwa w wojew\xf3dztwach \u015bl\u0105skimkatowickim, bielskim i cz\u0119stochowskim',
            'year': u'2009',
        }

        from recensio.policy.sparqlsearch import getMetadata
        metadata = getMetadata('9788361458258')
        metadata.pop('authors')
        self.assertEquals(expected, metadata)
        self.assertFalse([x.getMessage() for x in self.handler.records])

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

        from recensio.policy.sparqlsearch import getMetadata
        metadata = getMetadata('00157902')
        metadata.pop('authors')
        self.assertEquals(expected, metadata)
        self.assertFalse([x.getMessage() for x in self.handler.records])
