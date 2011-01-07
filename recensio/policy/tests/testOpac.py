# coding=utf8
import unittest2 as unittest
from BeautifulSoup import BeautifulSoup
from recensio.policy.opacsearch import OpacSearch, getString, createResult

sampleblob = '''<tr>
            <td>
                    
                    
        
                
            
            
                
                
            
                <strong class="c2">Verfasser: </strong>Pelletier, Michel&nbsp;; Latteier, Amos<br>

                <strong class="c2">Titel: </strong>¬The¬ ZOPE Book &lt;dt.&gt;|¬Das¬ ZOPE-Buch|Einführung und Dokumentation zur Entwicklung von Webanwendungen<br>

<strong class="c2">Impressum: </strong>München/Germany: Markt+Technik-Verl.: 2002: 380S., [8] Bl. : Ill., graph. Darst.<br>

<strong class="c2">ISBN/ISMN: </strong>3827261945<br>

<strong class="c2">Jahr: </strong>2002<br>

<strong class="c2">Zusatzinformationen: </strong>96319240X, Michel Pelletier ; Amos Latteier, CD-ROM (12 cm), New technology<br>

<strong class="c2">Dokumenttyp: </strong>Monographie<br>

<strong class="c2">BVB-Nummer: </strong>BV014063539<br>

<strong class="c2">Notation: </strong>ST 201 W78, Z:14, ST 201, ST 200, ST 253 Z91, ST 201 Z91, DAT 614f, DAT 309f, DAT 370f<br>


                <strong class="c2">Sprache: </strong>Deutsch<br>

                <br>


                
                
                
                
                

                

                <strong class="c2">Schlagwörter 1: </strong>Zope &lt;Programm&gt;<br><strong class="c2">Schlagwörter 2: </strong>World Wide Web&nbsp;; Server<br>

                
                
                
            
            </td>
        </tr>'''

class TestOpacSearch(unittest.TestCase):
    def testSuccessfulSearch(self):
        opac = OpacSearch()
        is_ = opac.getMetadataForISBN('3-8272-6194-5')
        should_be = [{'publisher': u'Markt+Technik-Verl.',
            'subtitle': u'Das ZOPE-Buch|Einf\xfchrung und Dokumentation zur Entwicklung von Webanwendungen',
            'location': u'M\xfcnchen/Germany',
            'language': u'Deutsch',
            'title': u'The ZOPE Book <dt.>',
            'ddc': None,
            'isbn': u'3827261945',
            'keywords' : [u'World Wide Web', u'Zope <Programm>', u'Server'],
            'authors': [{'firstname': u'Michel', 'lastname': u'Pelletier'},
               {'firstname': u'Amos', 'lastname': u'Latteier'}],
            'year': u'2002', 'pages': '437'}]
        self.assertEquals(should_be, is_)

    def testUnsuccessfulSearch(self):
        opac = OpacSearch()
        is_ = opac.getMetadataForISBN('')
        should_be = []
        self.assertEquals(should_be, is_)

    def testSuccessfulSearchFunnyISBN(self):
        opac = OpacSearch()
        is_1 = opac.getMetadataForISBN('3-8272-6194-5')
        is_2 = opac.getMetadataForISBN('3-8272-61945')
        is_3 = opac.getMetadataForISBN('3827261945')
        should_be = [{'publisher': u'Markt+Technik-Verl.',
            'subtitle': u'Das ZOPE-Buch|Einf\xfchrung und Dokumentation zur Entwicklung von Webanwendungen',
            'location': u'M\xfcnchen/Germany',
            'language': u'Deutsch',
            'title': u'The ZOPE Book <dt.>',
            'ddc': None,
            'isbn': u'3827261945',
            'keywords' : [u'World Wide Web', u'Zope <Programm>', u'Server'],
            'authors': [{'firstname': u'Michel', 'lastname': u'Pelletier'},
               {'firstname': u'Amos', 'lastname': u'Latteier'}],
            'year': u'2002', 'pages': '437'}]
        self.assertEquals(should_be, is_1)
        self.assertEquals(is_1, is_2)
        self.assertEquals(is_1, is_3)

    def testOpacDown(self):
        self.assertRaises(IOError, OpacSearch, 'http://www.syslab.com2')
        opac = OpacSearch('http://www.syslab.com')
        self.assertRaises(IOError,  opac.getMetadataForISBN, '3-8272-6194-5')

    def testCreateResultTitle(self):
        soup1 = BeautifulSoup('<td><strong>Titel:</strong>Test</td>')
        soup2 = BeautifulSoup('')
        self.assertEquals('Test', createResult(soup1)['title'])
        self.assertEquals(None, createResult(soup2)['title'])

    def testCreateResultSubtitle(self):
        soup1 = BeautifulSoup('''<td><strong>Titel:</strong>
  
  
    Some Book|Einführung und Dokumentation zur Entwicklung von Webanwendungen<br><br>
  </td>''')
        soup2 = BeautifulSoup('')
        self.assertEquals(u'Einführung und Dokumentation zur Entwicklung von Webanwendungen', createResult(soup1)['subtitle'].strip())
        self.assertEquals(None, createResult(soup2)['subtitle'])

    def testMoreThanOneResult(self):
        opac = OpacSearch()
        is_ = opac.getMetadataForISBN('978-0-19-928007-0')
        should_be = [{'authors': [{'firstname': u'Anthony', 'lastname': u'McElligott'}],
  'ddc': [u'G:de', u'S:ge', u'Z:42'],
  'isbn': u'9780199280063 : 9780199280070',
  'keywords': [u'Geschichte 1918-1933', u'Weimarer Republik', u'Deutschland'],
  'language': u'Englisch',
  'location': u'Oxford [u.a.]',
  'pages': u'324',
  'publisher': u'Oxford Univ. Press',
  'subtitle': None,
  'title': u'Weimar Germany',
  'year': u'2010'},
 {'authors': [{'firstname': u'Anthony', 'lastname': u'McElligott'}],
  'ddc': [u'G:de', u'S:ge', u'Z:42'],
  'isbn': u'9780199280063 : 9780199280070',
  'keywords': [u'Geschichte 1918-1933', u'Weimarer Republik', u'Deutschland'],
  'language': u'EnglischLink ( Inhaltsverzeichnis)',
  'location': u'Oxford [u.a.]',
  'pages': u'324',
  'publisher': u'Oxford Univ. Press',
  'subtitle': None,
  'title': u'Weimar Germany',
  'year': u'2009'}]
        self.assertEquals(should_be, is_)



    def testAuthors(self):
        soup1 = BeautifulSoup(sampleblob)
        soup2 = BeautifulSoup(sampleblob.replace('Pelletier, Michel', 'Pelletier, Michel, Maier'))
        soup3 = BeautifulSoup('')
        is_ = createResult(soup1)['authors']
        is_.sort() 
        self.assertEquals([
            {'lastname' : u'Latteier', 'firstname' : u'Amos'},
            {'firstname' : u'Michel', 'lastname' : u'Pelletier'}],
          is_)
        is_ = createResult(soup2)['authors']
        is_.sort() 
        self.assertEquals([
            {'firstname': None, 'lastname': u'Pelletier, Michel, Maier'},
            {'firstname': u'Amos', 'lastname': u'Latteier'}],
          is_)
        self.assertEquals([], createResult(soup3)['authors'])

    def testLocationPublisherYear(self):
        soup1 = BeautifulSoup(sampleblob)
        soup2 = BeautifulSoup(sampleblob.replace('>München/Germany: Markt+Technik-Verl.: 2002: 380S., [8] Bl. : Ill., graph. Darst.', ''))
        soup3 = BeautifulSoup()
        soup1_res = createResult(soup1)
        soup2_res = createResult(soup2)
        soup3_res = createResult(soup3)
        self.assertEquals(u'München/Germany', soup1_res['location'])
        self.assertEquals(u'Markt+Technik-Verl.', soup1_res['publisher'])
        self.assertEquals(u'2002', soup1_res['year'])
        self.assertEquals(None, soup2_res['location'])
        self.assertEquals(None, soup2_res['publisher'])
        self.assertEquals(None, soup2_res['year'])
        self.assertEquals(None, soup3_res['location'])
        self.assertEquals(None, soup3_res['publisher'])
        self.assertEquals(None, soup3_res['year'])


    def testPages(self):
        soup1 = BeautifulSoup(sampleblob)
        soup2 = BeautifulSoup(sampleblob.replace('380S., [8]', 'XXX'))
        soup3 = BeautifulSoup()
        soup1_res = createResult(soup1)
        soup2_res = createResult(soup2)
        soup3_res = createResult(soup3)
        self.assertEquals('380', soup1_res['pages'])
        self.assertEquals(None, soup2_res['pages'])
        self.assertEquals(None, soup3_res['pages'])

    def testLanguage(self):
        soup1 = BeautifulSoup(sampleblob)
        soup2 = BeautifulSoup(sampleblob.replace('Deutsch', ''))
        soup3 = BeautifulSoup()
        soup1_res = createResult(soup1)
        soup2_res = createResult(soup2)
        soup3_res = createResult(soup3)
        self.assertEquals('Deutsch', soup1_res['language'])
        self.assertEquals(None, soup2_res['language'])
        self.assertEquals(None, soup3_res['language'])

    def testDDC(self):
        soup1 = BeautifulSoup(sampleblob)
        soup2 = BeautifulSoup()
        soup1_res = createResult(soup1)
        soup2_res = createResult(soup2)
        self.assertEquals([u'Z:14'], soup1_res['ddc'])
        self.assertEquals(None, soup2_res['ddc'])

    def testKeywords(self):
        soup1 = BeautifulSoup(sampleblob)
        soup2 = BeautifulSoup()
        soup1_res = createResult(soup1)
        soup2_res = createResult(soup2)
        self.assertEquals([u'World Wide Web', u'Zope <Programm>', u'Server'], soup1_res['keywords'])
        self.assertEquals([], soup2_res['keywords'])

    def testISBN(self):
        soup1 = BeautifulSoup(sampleblob)
        soup2 = BeautifulSoup(sampleblob.replace('3827261945', ''))
        soup3 = BeautifulSoup()
        soup1_res = createResult(soup1)
        soup2_res = createResult(soup2)
        soup3_res = createResult(soup3)
        self.assertEquals('3827261945', soup1_res['isbn'])
        self.assertEquals(None, soup2_res['isbn'])
        self.assertEquals(None, soup3_res['isbn'])

    def testGetString(self):
        is_ = getString(BeautifulSoup('''<strong>  Text
<!-- Comment --></strong>''')).strip()
        should_be = 'Text'
        self.assertEquals(should_be,is_)
