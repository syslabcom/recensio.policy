#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest2 as unittest

import logging
from zope.testing.loggingsupport import InstalledHandler


class TestSparql(unittest.TestCase):

    def setUp(self):
        self.handler = InstalledHandler('recensio')
        self.maxDiff = 2000

    def tearDown(self):
        pass
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
            'language': u'Undetermined',
            'location': u'K\xf8benhavn',
            'pages': u'223',
            'publisher': None,
            'subtitle': None,
            'title': u'Structural studies in the Pre-Cambrian of western Greenland. 2: Geology of Tovqussap Nun\xe1',
            'year': u'1960',
            }

        is_ = getMetadata('123')
        is_.pop('authors')

        self.assertEquals(expected, is_)

    def testGetMetadata(self):
        from recensio.policy.sparqlsearch import getMetadata

        # http://lod.b3kat.de/title/BV035724519

        expected = {
            'authors': [],
            'ddc': u'372.6049',
            'isbn': u'9783830921929',
            'keywords': [u'Kindertagesst\xe4tte',
                         u'Kindertagesst\xe4tte - Spracherziehung - Kongress - Recklinghausen <2008>'
                         , u'Kongress', u'Spracherziehung'],
            'language': u'Undetermined',
            'location': u'M\xfcnster ; New York NY ; M\xfcnchen ; Berlin',
            'pages': u'162',
            'publisher': u'Waxmann',
            'subtitle': None,
            'title': u'Kinder bilden Sprache - Sprache bildet Kinder : Sprachentwicklung und Sprachf\xf6rderung in Kindertagesst\xe4tten ; [anl\xe4sslich des Landeskongresses "Kinder Bilden Sprache - Sprache Bildet Kinder" am 4. November 2008 in Recklinghausen]',
            'year': u'2009',
            }

        self.assertEquals(expected, getMetadata('9783830921929'))
        self.assertFalse([x.msg for x in self.handler.records])

    def testGetMetadata2(self):
        expected = {
            'ddc': u'900',
            'isbn': u'9780199280070',
            'keywords': [u'Deutschland', u'Geschichte 1918-1933',
                         u'Weimarer Republik'],
            'language': u'Undetermined',
            'location': u'Oxford [u.a.]',
            'pages': u'324',
            'publisher': u'Oxford Univ. Press',
            'subtitle': None,
            'title': u'Weimar Germany',
            'year': u'2010',
            }

        from recensio.policy.sparqlsearch import getMetadata
        metadata = getMetadata('978-0-19-928007-0')
        metadata.pop('authors')
        self.assertEquals(expected, metadata)
        self.assertFalse([x.msg for x in self.handler.records])
