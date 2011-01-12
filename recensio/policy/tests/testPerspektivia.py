import unittest2 as unittest
import pkg_resources
import datetime

from recensio.policy import importOAI
from recensio.policy.importOAI import perspektivia_parser

testdata_filename = pkg_resources.resource_filename(__name__, 'perspektivia.xml')
testdata2_filename = pkg_resources.resource_filename(__name__, 'perspektivia2.xml')

class TestPerspektiviaImport(unittest.TestCase):
    def testImportGood(self):
        should_be = {'books': [{'creator': [{'firstname': 'Dieter R.', 'lastname': 'Bauer'},
                        {'firstname': 'Johannes', 'lastname': 'Dillinger'},
                        {'firstname': u'J\xfcrgen Michael',
                         'lastname': u'Schmidt'}],
            'date': datetime.datetime(2010, 6, 30, 0, 0),
            'format': 'application/html',
            'id': 'oai:perspectivia.net.dhi-paris.francia/francia-recensio/rev-books/2010/978-3-89534-732-0',
            'identifier': '978-3-89534-732-0',
            'publisher': u'Verlag f\xfcr Regionalgeschichte, Bielefeld',
            'relation': 'http://www.perspectivia.net/content/publikationen/francia/francia-recensio/2010-2/FN/bauer-et-al_pillorget',
            'rights': '',
            'source': '',
            'subject': [],
            'title': 'Hexenprozess und Staatsbildung/Witch-Trials and State-Building',
            'type': 'Book'}],
 'reviews': [{'creator': [{'firstname': u'Ren\xe9',
                           'lastname': u'Pillorget'}],
              'date': datetime.datetime(2010, 6, 2, 0, 0),
              'format': 'application/html',
              'id': 'oai:perspectivia.net.dhi-paris.francia/francia-recensio/2010-2/FN/bauer-et-al_pillorget',
              'identifier': 'http://www.perspectivia.net/content/publikationen/francia/francia-recensio/2010-2/FN/bauer-et-al_pillorget',
              'publisher': 'perspectivia.net',
              'relation': '978-3-89534-732-0',
              'rights': 'by-nc-ne-3.0-de, perspectivia.net',
              'source': u'Perspectivia.net, Francia Recensio 2010-2, Fr\xfche Neuzeit \u2013 Revolution \u2013 Empire (1500\u20131815)',
              'subject': ['340.09',
                          't1.09024',
                          't1.09031',
                          't1.09032',
                          '940',
                          'Hexenverfolgung',
                          'Staat'],
              'title': u'D. Bauer, J. Dillinger, J. Schmidt, Hexenprozess und Staatsbildung (Ren\xe9 Pillorget)',
              'type': 'Review'}]}

        data = perspektivia_parser.parse(file(testdata_filename).read())
        self.assertEquals(data, should_be)

    def testRealDataCanPickle(self):
        data = perspektivia_parser.parse(file(testdata2_filename).read())
        import pickle
        for x in data['books'] + data['reviews']:
            pickle.dumps(x)

    def testRealDataIsEnough(self):
        data = perspektivia_parser.parse(file(testdata2_filename).read())
        self.assertEquals(997, len(data['books']), "Not enough books?")
        self.assertEquals(919, len(data['reviews']))
