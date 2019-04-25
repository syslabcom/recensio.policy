# -*- coding: utf-8 -*-
from mock import patch
from recensio.policy.srusearch import getMetadata
import os
import unittest2 as unittest


class MockResultFactory(object):
    def __init__(self, filename):
        with open(
            os.path.join(os.path.dirname(__file__), filename),
            'r',
        ) as mock_data_file:
            self.mock_data = mock_data_file.read()

    def __call__(self, dummy):
        return self.mock_data


class TestSRU(unittest.TestCase):

    def test_sru_isbn_123(self):
        expected = {
            'bv': u'BV013575871',
            'authors': ['Berthelsen, Asger'],
            'ddcPlace': [],
            'ddcSubject': [],
            'ddcTime': [],
            'isbn': u'123',
            'keywords': [],
            'language': u'English',
            'location': u'K\xf8benhavn',
            'pages': u'223 S.',
            'publisher': None,
            'series': u'2; Grønlands Geologiske Undersøgelse: Bulletin',
            'seriesVol': u'25',
            'subtitle': None,
            'title': u'Structural studies in the Pre-Cambrian of western Greenland',
            'year': u'1960',
        }
        filename = 'sru_data_123.xml'
        with patch(
            'recensio.policy.srusearch.fetchMetadata',
            side_effect=MockResultFactory(filename),
        ):
            md = getMetadata('123')
        self.assertEquals(expected, md)

    def test_sru_isbn_9783830921929(self):
        self.maxDiff = None
        expected = {
            'bv': u'BV035724519',
            'authors': [],
            'ddcPlace': [],
            'ddcSubject': [u'372.6049'],
            'ddcTime': [],
            'isbn': u'9783830921929',
            'keywords': [
                u'Spracherziehung',
                u'Konferenzschrift',
                u'Kindertagesst\xe4tte',
                u'Kindertagesst\xe4tte - Spracherziehung - Kongress - Recklinghausen <2008>',
            ],
            'language': u'German',
            'location': u'M\xfcnster ; New York, NY ; M\xfcnchen ; Berlin',
            'pages': u'162 S.',
            'publisher': u'Waxmann',
            'series': None,
            'seriesVol': None,
            'subtitle': u'Sprachentwicklung und Sprachf\xf6rderung in Kindertagesst\xe4tten ; [anl\xe4sslich des Landeskongresses \"Kinder Bilden Sprache - Sprache Bildet Kinder\" am 4. November 2008 in Recklinghausen]',
            'title': u'Kinder bilden Sprache - Sprache bildet Kinder',

            'year': u'2009',
        }
        filename = 'sru_data_9783830921929.xml'
        with patch(
            'recensio.policy.srusearch.fetchMetadata',
            side_effect=MockResultFactory(filename),
        ):
            md = getMetadata('9783830921929')
        self.assertEquals(expected, md)

    def test_sru_isbn_9780199280070(self):
        self.maxDiff = None
        expected = {
            'bv': u'BV036604193',  # XXX second entry: u'BV035356471',
            'authors': [],
            'ddcPlace': [],
            'ddcSubject': [u'943.085'],
            'ddcTime': [],
            'isbn': u'9780199280070',
            'keywords': [
                u'Germany',
                u'Geschichte 1918-1933',
                u'Weimarer Republik',
                u'Deutschland',
                u'Geschichte',
            ],
            'language': u'English',
            'location': u'Oxford [u.a.]',
            'pages': u'XVIII, 324 S.',
            'publisher': u'Oxford Univ. Press',
            'series': u'\x98The\x9c short Oxford history of Germany',
            'seriesVol': None,
            'subtitle': None,
            'title': u'Weimar Germany',
            'year': u'2010',
        }
        filename = 'sru_data_9780199280070.xml'
        with patch(
            'recensio.policy.srusearch.fetchMetadata',
            side_effect=MockResultFactory(filename),
        ):
            md = getMetadata('978-0-19-928007-0')
        self.assertEquals(expected, md)

    def test_sru_isbn_9783863864880(self):
        self.maxDiff = None
        expected = {
            'bv': u'BV041201260',
            'authors': [u'Kraus, Eva', ],
            'ddcPlace': [],  # XXX [u'43'],
            'ddcSubject': [],  # XXX [u'306.09'],
            'ddcTime': [],  # XXX [u'09041', u'09042', ],
            'isbn': u'9783863864880',
            'keywords': [
                u'Deutsches Jugendherbergswerk',
                u'Schirrmann, Richard',
                u'Hochschulschrift',
                u'Deutschland/Deutsches Jugendherbergswerk',
                u'Deutschland',
                u'Geschichte 1933',
                u'Weltanschauung',
                u'Reichsverband f\xfcr Deutsche Jugendherbergen',
                u'Persönlichkeit, Politik',
                u'Geschichte',
                u'Geschichte 1909-1932',
                u'Geschichte 1909-1933',
                u'Jugendbewegung',
                u'Bayern',
                u'Gleichschaltung',
                u'Nationalsozialismus',
                u'Jugendherberge',
            ],
            'language': u'German',
            'location': u'Berlin',
            'pages': u'450 S.',
            'publisher': u'Pro Business',
            'series': None,
            'seriesVol': None,
            'subtitle': u'1909 - 1933 ; Programm - Personen - Gleichschaltung',
            'title': u'\x98Das\x9c Deutsche Jugendherbergswerk',
            'year': u'2013',
        }
        filename = 'sru_data_9783863864880.xml'
        with patch(
            'recensio.policy.srusearch.fetchMetadata',
            side_effect=MockResultFactory(filename),
        ):
            md = getMetadata('978-3-86386-488-0')
        self.assertEquals(expected, md)
