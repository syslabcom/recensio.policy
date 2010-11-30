import unittest2 as unittest
import pkg_resources

from recensio.policy import importSehepunkte
from recensio.policy.importSehepunkte import sehepunkte_parser

testdata_filename = pkg_resources.resource_filename(__name__, \
    'testSehepunkte.xml')
testdata_parsed = [{'authors': [{'firstname': 'Mathias', 'lastname': 'Piana'}],
  'category': 'Kunstgeschichte',
  'isbn': '978-3-86568-039-6',
  'issue': '11',
  'pages': '495',
  'placeOfPublication': 'Petersberg',
  'publisher': 'Michael Imhof Verlag',
  'reviewAuthorFirstname': 'Lorenz',
  'reviewAuthorLastname': 'Korn',
  'series': 'Studien zur internationalen Architektur- und Kunstgeschichte',
  'subtitle': '',
  'title': u'Burgen und St\xe4dte der Kreuzzugszeit',
  'uri': 'http://www.sehepunkte.de/export/rezension_17542.html',
  'volume': '10',
  'year': '2010'},
 {'authors': [{'firstname': 'Hans', 'lastname': 'Belting'}],
  'category': 'Kunstgeschichte',
  'isbn': '978-3-406-57092-6',
  'issue': '11',
  'pages': '319',
  'placeOfPublication': u'M\xfcnchen',
  'publisher': 'C.H.Beck',
  'reviewAuthorFirstname': 'Lorenz',
  'reviewAuthorLastname': 'Korn',
  'series': '',
  'subtitle': u'Eine west\xf6stliche Geschichte des Blicks',
  'title': 'Florenz und Bagdad',
  'uri': 'http://www.sehepunkte.de/export/rezension_17750.html',
  'volume': '10',
  'year': '2010'},
 {'authors': [{'firstname': 'Jonathan M.', 'lastname': 'Bloom'},
              {'firstname': 'Sheila S.', 'lastname': 'Blair'}],
  'category': 'Kunstgeschichte',
  'isbn': '978-0-19-530991-1',
  'issue': '11',
  'pages': 'CII + 1586',
  'placeOfPublication': 'Oxford',
  'publisher': 'Oxford University Press',
  'reviewAuthorFirstname': 'Lorenz',
  'reviewAuthorLastname': 'Korn',
  'series': '',
  'subtitle': '',
  'title': 'The Grove Encyclopedia of Islamic Art and Architecture',
  'uri': 'http://www.sehepunkte.de/export/rezension_17543.html',
  'volume': '10',
  'year': '2010'},
 {'authors': [{'firstname': '', 'lastname': 'Museum with no Frontiers'}],
  'category': 'Kunstgeschichte',
  'isbn': '',
  'issue': '11',
  'pages': '',
  'placeOfPublication': '',
  'publisher': '',
  'reviewAuthorFirstname': 'Eva-Maria',
  'reviewAuthorLastname': 'Troelenberg',
  'series': '',
  'subtitle': 'Webportal. URL: http://www.discoverislamicart.org',
  'title': 'Discover Islamic Art',
  'uri': 'http://www.sehepunkte.de/export/rezension_18515.html',
  'volume': '10',
  'year': '2010'},
 {'authors': [{'firstname': 'Ellen', 'lastname': 'Kenney'}],
  'category': 'Kunstgeschichte',
  'isbn': '978-0-9708199-4-9',
  'issue': '11',
  'pages': 'XIV + 257',
  'placeOfPublication': 'Chicago',
  'publisher': 'Chicago Studies on the Middle East',
  'reviewAuthorFirstname': 'Verena',
  'reviewAuthorLastname': 'Daiber',
  'series': 'Chicago Studies on the Middle East',
  'subtitle': 'The Architecture and Urban Works of Tankiz Al-Nasiri',
  'title': 'Power and Patronage in Medieval Syria',
  'uri': 'http://www.sehepunkte.de/export/rezension_17779.html',
  'volume': '10',
  'year': '2010'},
 {'authors': [{'firstname': 'ChristianJulia', 'lastname': 'EwertGonnella'},
              {'firstname': 'Jens', 'lastname': u'Kr\xf6ger'}],
  'category': 'Kunstgeschichte',
  'isbn': '978-3-88609-564-3978-3-930454-82-2',
  'issue': '11',
  'pages': '143XXIV + 197',
  'placeOfPublication': u'BerlinM\xfcnster',
  'publisher': u'Staatliche Museen Preu\xdfischer KulturbesitzRhema Verlag',
  'reviewAuthorFirstname': 'Verena',
  'reviewAuthorLastname': 'Daiber',
  'series': 'Forschungen zur Islamischen Kunstgeschichte. Neue Folge',
  'subtitle': u'Strukturen und Dekorelemente der Malereien im Aleppozimmer des Museums f\xfcr Islamische Kunst in BerlinThe Aleppo Room in Berlin. International Symposium of the Museum f\xfcr Islamische Kunst - Staatliche Museen zu Berlin 12.-14. April 2002',
  'title': 'Das AleppozimmerAngels, Peonies, and Fabulous Creatures',
  'uri': 'http://www.sehepunkte.de/export/rezension_17746.html',
  'volume': '10',
  'year': '2010'},
 {'authors': [{'firstname': 'Christiane J.', 'lastname': 'Gruber'}],
  'category': 'Kunstgeschichte',
  'isbn': '978-84-95061-29-4',
  'issue': '11',
  'pages': '432',
  'placeOfPublication': 'Valencia',
  'publisher': 'Patrimonio Ediciones',
  'reviewAuthorFirstname': 'Vera',
  'reviewAuthorLastname': 'Beyer',
  'series': '',
  'subtitle': 'A Study of Text and Image in a Pan-Asian Context',
  'title': u'El Libro de la Ascensi\xf3n Mi&#703;rajnama Tim\xfarida. The Timurid Book of Ascension (Mi&#703;rajnama)',
  'uri': 'http://www.sehepunkte.de/export/rezension_19127.html',
  'volume': '10',
  'year': '2010'},
 {'authors': [{'firstname': 'Adnan', 'lastname': 'Shiyyab'}],
  'category': 'Kunstgeschichte',
  'isbn': '978-3-8316-0545-3',
  'issue': '11',
  'pages': '328',
  'placeOfPublication': u'M\xfcnchen',
  'publisher': 'Herbert Utz Verlag',
  'reviewAuthorFirstname': 'Ute',
  'reviewAuthorLastname': 'Verstegen',
  'series': 'Kunstwissenschaften',
  'subtitle': u"Arch\xe4ologische und kunstgeschichtliche Untersuchungen unter besonderer Ber\xfccksichtigung der \xbbKirche von Ya'mun\xab",
  'title': u'Der Islam und der Bilderstreit in Jordanien und Pal\xe4stina',
  'uri': 'http://www.sehepunkte.de/export/rezension_17270.html',
  'volume': '10',
  'year': '2010'},
 {'authors': [{'firstname': 'Wolfgang', 'lastname': 'Sellert'},
              {'firstname': 'Ursula', 'lastname': 'Machoczek'}],
  'category': u'Fr\xfche Neuzeit',
  'isbn': '978-3-503-09886-6',
  'issue': '11',
  'pages': '773',
  'placeOfPublication': 'Berlin',
  'publisher': 'Erich Schmidt Verlag',
  'reviewAuthorFirstname': 'Anja',
  'reviewAuthorLastname': 'Amend-Traut',
  'series': '',
  'subtitle': 'Serie II: Antiqua Band 1: Karton 1-43',
  'title': 'Die Akten des kaiserlichen Reichshofrats (RHR)',
  'uri': 'http://www.sehepunkte.de/export/rezension_17657.html',
  'volume': '10',
  'year': '2010'},
 {'authors': [{'firstname': 'Larissa', 'lastname': u'F\xf6rster'}],
  'category': 'Zeitgeschichte',
  'isbn': '978-3-593-391601',
  'issue': '11',
  'pages': '391',
  'placeOfPublication': 'Frankfurt/M.',
  'publisher': 'Campus',
  'reviewAuthorFirstname': u'D\xf6rte',
  'reviewAuthorLastname': 'Lerp',
  'series': '',
  'subtitle': 'Wie Deutsche und Herero in Namibia des Kriegs von 1904 gedenken',
  'title': 'Postkoloniale Erinnerungslandschaften',
  'uri': 'http://www.sehepunkte.de/export/rezension_17739.html',
  'volume': '10',
  'year': '2010'},
 {'authors': [{'firstname': 'Efrem', 'lastname': 'Zambon'}],
  'category': 'Altertum',
  'isbn': '978-3-515-09194-7',
  'issue': '11',
  'pages': '326',
  'placeOfPublication': 'Stuttgart',
  'publisher': 'Franz Steiner Verlag',
  'reviewAuthorFirstname': 'Caroline',
  'reviewAuthorLastname': 'Veit',
  'series': 'Historia. Einzelschriften',
  'subtitle': 'Sicily between Hellenism and Rome',
  'title': 'Tradition and Innovation',
  'uri': 'http://www.sehepunkte.de/export/rezension_15037.html',
  'volume': '10',
  'year': '2010'},
 {'authors': [{'firstname': 'Holger', 'lastname': u'L\xf6ttel'}],
  'category': '19. Jahrhundert',
  'isbn': '978-3-515-09334-7',
  'issue': '11',
  'pages': '468',
  'placeOfPublication': 'Stuttgart',
  'publisher': 'Franz Steiner Verlag',
  'reviewAuthorFirstname': 'John Andreas',
  'reviewAuthorLastname': 'Fuchs',
  'series': 'Transatlantische Historische Studien',
  'subtitle': u'Englandbilder im amerikanischen S\xfcden und die Au\xdfenpolitik der Konf\xf6deration',
  'title': 'Um Ehre und Anerkennung',
  'uri': 'http://www.sehepunkte.de/export/rezension_17203.html',
  'volume': '10',
  'year': '2010'},
 {'authors': [{'firstname': 'Paul', 'lastname': 'Griffiths'}],
  'category': u'Fr\xfche Neuzeit',
  'isbn': '978-0-521-88524-9',
  'issue': '11',
  'pages': 'XVII + 544',
  'placeOfPublication': 'Cambridge',
  'publisher': 'Cambridge University Press',
  'reviewAuthorFirstname': u'Andr\xe9',
  'reviewAuthorLastname': 'Krischer',
  'series': 'Cambridge Social and Cultural Histories',
  'subtitle': 'Change, Crime, and Control in the Capital City, 1550-1660',
  'title': 'Lost Londons',
  'uri': 'http://www.sehepunkte.de/export/rezension_16539.html',
  'volume': '10',
  'year': '2010'},
 {'authors': [{'firstname': 'Robert', 'lastname': 'Bees'}],
  'category': 'Altertum',
  'isbn': '978-3-406-58804-4',
  'issue': '11',
  'pages': '320',
  'placeOfPublication': u'M\xfcnchen',
  'publisher': 'C.H.Beck',
  'reviewAuthorFirstname': 'Claas',
  'reviewAuthorLastname': 'Lattmann',
  'series': 'Zetemata. Monographien zur klassischen Altertumswissenschaft',
  'subtitle': u'Interpretationen zum Verst\xe4ndnis seiner Theologie',
  'title': 'Aischylos',
  'uri': 'http://www.sehepunkte.de/export/rezension_16440.html',
  'volume': '10',
  'year': '2010'},
 {'authors': [{'firstname': 'Keith', 'lastname': 'Sidwell'}],
  'category': 'Altertum',
  'isbn': '978-0-521-51998-4',
  'issue': '11',
  'pages': 'XV + 407',
  'placeOfPublication': 'Cambridge',
  'publisher': 'Cambridge University Press',
  'reviewAuthorFirstname': 'Johannes',
  'reviewAuthorLastname': 'Engels',
  'series': '',
  'subtitle': 'The Politics of Satirical Comedy during the Peloponnesian War',
  'title': 'Aristophanes the Democrat',
  'uri': 'http://www.sehepunkte.de/export/rezension_17278.html',
  'volume': '10',
  'year': '2010'},
 {'authors': [{'firstname': 'Sebastian', 'lastname': 'Joost'}],
  'category': u'Fr\xfche Neuzeit',
  'isbn': '978-3-8258-1062-7',
  'issue': '11',
  'pages': '270',
  'placeOfPublication': u'M\xfcnster / Hamburg / Berlin / London',
  'publisher': 'LIT',
  'reviewAuthorFirstname': 'Dirk',
  'reviewAuthorLastname': 'Schleinert',
  'series': 'Rostocker Schriften zur Regionalgeschichte',
  'subtitle': u'Ausw\xe4rtige Politik als Mittel zur Durchsetzung landesherrlicher Macht in Mecklenburg (1648-1695)',
  'title': 'Zwischen Hoffnung und Ohnmacht',
  'uri': 'http://www.sehepunkte.de/export/rezension_15377.html',
  'volume': '10',
  'year': '2010'},
 {'authors': [{'firstname': 'Pit', 'lastname': u'P\xe9port\xe9'},
              {'firstname': 'Sonja', 'lastname': 'Kmec'},
              {'firstname': u'Beno\xeet', 'lastname': 'Majerus'}],
  'category': '19. Jahrhundert',
  'isbn': '978-90-04-18176-2',
  'issue': '11',
  'pages': 'XII + 383',
  'placeOfPublication': 'Leiden / Boston / Tokyo',
  'publisher': 'Brill Academic Publishers',
  'reviewAuthorFirstname': 'Norbert',
  'reviewAuthorLastname': 'Franz',
  'series': 'National Cultivation of Culture',
  'subtitle': 'Representations of the Past, Space and Language from the Nineteenth to the Twenty-First Century',
  'title': 'Inventing Luxembourg',
  'uri': 'http://www.sehepunkte.de/export/rezension_17942.html',
  'volume': '10',
  'year': '2010'},
 {'authors': [{'firstname': 'Sven Oliver', 'lastname': u'M\xfcller'},
              {'firstname': 'Philipp', 'lastname': 'Ther'},
              {'firstname': 'Jutta', 'lastname': 'Toelle'}],
  'category': u'Epochen\xfcbergreifend',
  'isbn': '978-3-486-59236-8',
  'issue': '11',
  'pages': '331',
  'placeOfPublication': u'M\xfcnchen',
  'publisher': 'Oldenbourg',
  'reviewAuthorFirstname': 'Boris',
  'reviewAuthorLastname': 'Slamka',
  'series': u'Die Gesellschaft der Oper. Musikkultur europ\xe4ischer Metropolen im 19. und 20. Jahrhundert',
  'subtitle': 'Kulturtransfers und Netzwerke des Musiktheaters in Europa',
  'title': 'Die Oper im Wandel der Gesellschaft',
  'uri': 'http://www.sehepunkte.de/export/rezension_17686.html',
  'volume': '10',
  'year': '2010'},
 {'authors': [{'firstname': 'Gilles', 'lastname': 'Gorre'}],
  'category': 'Altertum',
  'isbn': '978-9-0429-2035-4',
  'issue': '11',
  'pages': 'LVIII + 641',
  'placeOfPublication': 'Leuven',
  'publisher': 'Peeters',
  'reviewAuthorFirstname': 'Arthur',
  'reviewAuthorLastname': 'Verhoogt',
  'series': 'Studia Hellenistica',
  'subtitle': '',
  'title': u"Les relations du clerg\xe9 \xe9gyptien et des lagides d'apr\xe8s des sources priv\xe9es",
  'uri': 'http://www.sehepunkte.de/export/rezension_17187.html',
  'volume': '10',
  'year': '2010'},
 {'authors': [{'firstname': 'Michael', 'lastname': 'Maaser'}],
  'category': u'Fr\xfche Neuzeit',
  'isbn': '978-3-515-09177-0',
  'issue': '11',
  'pages': '222',
  'placeOfPublication': 'Stuttgart',
  'publisher': 'Franz Steiner Verlag',
  'reviewAuthorFirstname': 'Elizabeth',
  'reviewAuthorLastname': 'Harding',
  'series': 'Frankfurter Historische Abhandlungen',
  'subtitle': u'Herzog Julius (1528-1589) und die Universit\xe4t Helmstedt',
  'title': 'Humanismus und Landesherrschaft',
  'uri': 'http://www.sehepunkte.de/export/rezension_18641.html',
  'volume': '10',
  'year': '2010'},
 {'authors': [{'firstname': 'Finbarr B.', 'lastname': 'Flood'}],
  'category': 'Kunstgeschichte',
  'isbn': '978-0-6911-2594-7',
  'issue': '11',
  'pages': 'XV + 366',
  'placeOfPublication': 'Princeton / Oxford',
  'publisher': 'Princeton University Press',
  'reviewAuthorFirstname': 'Daniel',
  'reviewAuthorLastname': 'Redlinger',
  'series': '',
  'subtitle': 'Material Culture and Medieval "Hindu-Muslim" Encounter',
  'title': 'Objects of Translation',
  'uri': 'http://www.sehepunkte.de/export/rezension_17748.html',
  'volume': '10',
  'year': '2010'},
 {'authors': [{'firstname': 'Karin', 'lastname': 'Bartl'},
              {'firstname': 'Abd al-Razzaq', 'lastname': 'Moaz'}],
  'category': 'Kunstgeschichte',
  'isbn': '978-3-89646-654-9',
  'issue': '11',
  'pages': 'XVI + 541',
  'placeOfPublication': 'Rahden/Westf.',
  'publisher': 'Verlag Marie Leidorf',
  'reviewAuthorFirstname': 'Mustafa',
  'reviewAuthorLastname': 'Tupev',
  'series': u'Orient-Arch\xe4ologie',
  'subtitle': u'Transformationsprozesse von der Sp\xe4tantike bis in fr\xfchislamische Zeit in Bilad as-Sham. Beitr\xe4ge des Internationalen Kolloquiums in Damaskus vom 5.-9. November 2006',
  'title': 'Residenzen, Befestigungen, Siedlungen',
  'uri': 'http://www.sehepunkte.de/export/rezension_17744.html',
  'volume': '10',
  'year': '2010'},
 {'authors': [{'firstname': 'Lorenz', 'lastname': 'Korn'},
              {'firstname': 'Markus', 'lastname': 'Ritter'}],
  'category': 'Kunstgeschichte',
  'isbn': '978-3-89500-766-8',
  'issue': '11',
  'pages': '246',
  'placeOfPublication': 'Wiesbaden',
  'publisher': 'Reichert Verlag',
  'reviewAuthorFirstname': 'Jens',
  'reviewAuthorLastname': u'Kr\xf6ger (i.R.)',
  'series': 'Jahrbuch der Ernst-Herzfeld-Gesellschaft e.V.',
  'subtitle': '',
  'title': u'Beitr\xe4ge zur islamischen Kunst und Arch\xe4ologie Band 2',
  'uri': 'http://www.sehepunkte.de/export/rezension_18635.html',
  'volume': '10',
  'year': '2010'},
 {'authors': [{'firstname': 'RobertMahmoud K.',
               'lastname': 'HillenbrandHawari'},
              {'firstname': 'Sylvia', 'lastname': 'Auld'}],
  'category': 'Kunstgeschichte',
  'isbn': '978-1-901435-06-1978-1-4073-0042-9',
  'issue': '11',
  'pages': 'x + 517XXI + 214',
  'placeOfPublication': 'LondonOxford',
  'publisher': 'Altajir TrustArchaeopress',
  'reviewAuthorFirstname': 'Mathias',
  'reviewAuthorLastname': 'Piana',
  'series': 'BAR International Series',
  'subtitle': 'The Holy City in Context 1187-1250An architectural and archaeological study',
  'title': 'Ayyubid JerusalemAyyubid Jerusalem (1187 - 1250)',
  'uri': 'http://www.sehepunkte.de/export/rezension_18634.html',
  'volume': '10',
  'year': '2010'},
 {'authors': [{'firstname': 'Werner', 'lastname': 'Freitag'},
              {'firstname': 'Christian', 'lastname': 'Helbich'}],
  'category': u'Fr\xfche Neuzeit',
  'isbn': '978-3-402-15043-6',
  'issue': '11',
  'pages': '318',
  'placeOfPublication': u'M\xfcnster',
  'publisher': 'Aschendorff',
  'reviewAuthorFirstname': 'Christoph',
  'reviewAuthorLastname': 'Nebgen',
  'series': u'Westfalen in der Vormoderne. Studien zur mittelalterlichen und fr\xfchneuzeitlichen Landesgeschichte',
  'subtitle': 'Neue Forschungen zu Reformation und Konfessionalisierung in Westfalen',
  'title': 'Bekenntnis, soziale Ordnung und rituelle Praxis',
  'uri': 'http://www.sehepunkte.de/export/rezension_18627.html',
  'volume': '10',
  'year': '2010'},
 {'authors': [{'firstname': 'Arndt', 'lastname': 'Brendecke'}],
  'category': u'Fr\xfche Neuzeit',
  'isbn': '978-3-412-20399-3',
  'issue': '11',
  'pages': '486',
  'placeOfPublication': u'K\xf6ln / Weimar / Wien',
  'publisher': u'B\xf6hlau',
  'reviewAuthorFirstname': 'Pedro',
  'reviewAuthorLastname': u'Mart\xednez Garc\xeda',
  'series': '',
  'subtitle': 'Funktion des Wissens in der spanischen Kolonialherrschaft',
  'title': 'Imperium und Empirie',
  'uri': 'http://www.sehepunkte.de/export/rezension_16636.html',
  'volume': '10',
  'year': '2010'},
 {'authors': [{'firstname': 'John', 'lastname': 'Darwin'}],
  'category': u'Epochen\xfcbergreifend',
  'isbn': '978-0-521-30208-1',
  'issue': '11',
  'pages': 'XIII + 800',
  'placeOfPublication': 'Cambridge',
  'publisher': 'Cambridge University Press',
  'reviewAuthorFirstname': 'Verena',
  'reviewAuthorLastname': 'Steller',
  'series': '',
  'subtitle': 'The Rise and Fall of the British World-Systen, 1830-1970',
  'title': 'The Empire Project',
  'uri': 'http://www.sehepunkte.de/export/rezension_16547.html',
  'volume': '10',
  'year': '2010'},
 {'authors': [{'firstname': u'J\xfcrgen Peter', 'lastname': 'Schmied'}],
  'category': 'Zeitgeschichte',
  'isbn': '978-3-406-60585-7',
  'issue': '11',
  'pages': '683',
  'placeOfPublication': u'M\xfcnchen',
  'publisher': 'C.H.Beck',
  'reviewAuthorFirstname': 'Florian',
  'reviewAuthorLastname': 'Keisinger',
  'series': '',
  'subtitle': 'Eine Biographie',
  'title': 'Sebastian Haffner',
  'uri': 'http://www.sehepunkte.de/export/rezension_18488.html',
  'volume': '10',
  'year': '2010'},
 {'authors': [{'firstname': 'Kai', 'lastname': 'Brodersen'},
              {'firstname': 'Ja&#347;', 'lastname': 'Elsner'}],
  'category': 'Altertum',
  'isbn': '978-3-515-09426-9',
  'issue': '11',
  'pages': '171',
  'placeOfPublication': 'Stuttgart',
  'publisher': 'Franz Steiner Verlag',
  'reviewAuthorFirstname': 'Stefano',
  'reviewAuthorLastname': 'Magnani',
  'series': 'Historia. Einzelschriften',
  'subtitle': "Working Papers on P.Artemid. (St. John's College Oxford, 2008)",
  'title': 'Images and Texts on the "Artemidorus Papyrus"',
  'uri': 'http://www.sehepunkte.de/export/rezension_17165.html',
  'volume': '10',
  'year': '2010'},
 {'authors': [{'firstname': 'Keith', 'lastname': 'Hamilton'},
              {'firstname': 'Patrick', 'lastname': 'Salmon'},
              {'firstname': 'Stephen', 'lastname': 'Twigge'}],
  'category': 'Zeitgeschichte',
  'isbn': '978-0-415-44870-3',
  'issue': '11',
  'pages': 'VIII + 119',
  'placeOfPublication': 'London / New York',
  'publisher': 'Routledge',
  'reviewAuthorFirstname': 'Dominik',
  'reviewAuthorLastname': 'Geppert',
  'series': '',
  'subtitle': 'Berlin in the Cold War, 1948-1990',
  'title': 'Documents on British Policy Overseas, Series III, Vol. VI',
  'uri': 'http://www.sehepunkte.de/export/rezension_14507.html',
  'volume': '10',
  'year': '2010'},
 {'authors': [{'firstname': 'Fritz J.', 'lastname': 'Raddatz'}],
  'category': 'Zeitgeschichte',
  'isbn': '978-3-498-05781-7',
  'issue': '11',
  'pages': '941',
  'placeOfPublication': 'Reinbek',
  'publisher': 'Rowohlt Verlag',
  'reviewAuthorFirstname': 'Florian',
  'reviewAuthorLastname': 'Keisinger',
  'series': '',
  'subtitle': 'Jahre 1982-2001',
  'title': u'Tageb\xfccher',
  'uri': 'http://www.sehepunkte.de/export/rezension_18783.html',
  'volume': '10',
  'year': '2010'},
 {'authors': [{'firstname': 'Annette', 'lastname': 'Jantzen'}],
  'category': '19. Jahrhundert',
  'isbn': '978-3-506-76873-5',
  'issue': '11',
  'pages': '367',
  'placeOfPublication': 'Paderborn',
  'publisher': u'Ferdinand Sch\xf6ningh',
  'reviewAuthorFirstname': 'Joachim',
  'reviewAuthorLastname': 'Schmiedl',
  'series': u'Ver\xf6ffentlichungen der Kommission f\xfcr Zeitgeschichte. Reihe B: Forschungen',
  'subtitle': u'Els\xe4ssische und franz\xf6sisch-lothringische Geistliche im Ersten Weltkrieg',
  'title': 'Priester im Krieg',
  'uri': 'http://www.sehepunkte.de/export/rezension_17733.html',
  'volume': '10',
  'year': '2010'},
 {'authors': [{'firstname': 'Jana', 'lastname': 'Osterkamp'}],
  'category': 'Zeitgeschichte',
  'isbn': '978-3-465-04073-6',
  'issue': '11',
  'pages': 'X + 310',
  'placeOfPublication': 'Frankfurt /M.',
  'publisher': 'Vittorio Klostermann',
  'reviewAuthorFirstname': 'Peter',
  'reviewAuthorLastname': 'Bugge',
  'series': u'Studien zur europ\xe4ischen Rechtsgeschichte',
  'subtitle': u'Verfassungsidee - Demokratieverst\xe4ndnis - Nationalit\xe4tenproblem',
  'title': 'Verfassungsgerichtsbarkeit in der Tschechoslowakei (1920-1939)',
  'uri': 'http://www.sehepunkte.de/export/rezension_19041.html',
  'volume': '10',
  'year': '2010'},
 {'authors': [{'firstname': 'Gertrude', 'lastname': 'Enderle-Burcel'},
              {'firstname': 'Piotr', 'lastname': 'Franaszek'},
              {'firstname': 'Dieter', 'lastname': 'Stiefel'}],
  'category': 'Zeitgeschichte',
  'isbn': '978-83-233-2532-1',
  'issue': '11',
  'pages': 'XVI + 293',
  'placeOfPublication': u'Krak\xf3w',
  'publisher': 'WUJ',
  'reviewAuthorFirstname': 'Uwe',
  'reviewAuthorLastname': u'M\xfcller',
  'series': '',
  'subtitle': 'Econnomic relations between neutral and socialist countries in Cold War Europe',
  'title': 'Gaps in the Iron Curtain',
  'uri': 'http://www.sehepunkte.de/export/rezension_19040.html',
  'volume': '10',
  'year': '2010'},
 {'authors': [{'firstname': 'Otfrid', 'lastname': 'Pustejovsky'}],
  'category': 'Zeitgeschichte',
  'isbn': '978-3-8258-1703-9',
  'issue': '11',
  'pages': '296',
  'placeOfPublication': u'M\xfcnster / Hamburg / Berlin / London',
  'publisher': 'LIT',
  'reviewAuthorFirstname': 'Martin',
  'reviewAuthorLastname': u'Z\xfcckert',
  'series': u'Beitr\xe4ge zu Theologie, Kirche und Gesellschaft im 20. Jahrhundert',
  'subtitle': u'Eine Bestandsaufnahme zu den Verh\xe4ltnissen im Sudetenland und dem Protektorat B\xf6hmen und M\xe4hren',
  'title': u'Christlicher Widerstand gegen die NS-Herrschaft in den B\xf6hmischen L\xe4ndern',
  'uri': 'http://www.sehepunkte.de/export/rezension_19039.html',
  'volume': '10',
  'year': '2010'},
 {'authors': [{'firstname': 'Tobias', 'lastname': 'Weger'}],
  'category': u'Epochen\xfcbergreifend',
  'isbn': '978-3-631-58554-2',
  'issue': '11',
  'pages': '513',
  'placeOfPublication': 'Bern / Frankfurt a.M. [u.a.]',
  'publisher': 'Peter Lang',
  'reviewAuthorFirstname': 'Stefan',
  'reviewAuthorLastname': 'Dyroff',
  'series': 'Mitteleuropa - Osteuropa',
  'subtitle': 'Wirkung - Interaktion - Rezeption',
  'title': u'Grenz\xfcberschreitende Biographien zwischen Ost- und Mitteleuropa',
  'uri': 'http://www.sehepunkte.de/export/rezension_19035.html',
  'volume': '10',
  'year': '2010'},
 {'authors': [{'firstname': 'Christine', 'lastname': 'Koch-Hallas'}],
  'category': 'Zeitgeschichte',
  'isbn': '978-3-374-02687-6',
  'issue': '11',
  'pages': '420',
  'placeOfPublication': 'Leipzig',
  'publisher': 'Evangelische Verlagsanstalt',
  'reviewAuthorFirstname': 'Martin',
  'reviewAuthorLastname': 'Greschat',
  'series': 'Arbeiten zur Kirchen- und Theologiegeschichte',
  'subtitle': u'Eine Untersuchung \xfcber Kontinuit\xe4ten und Diskontinuit\xe4ten einer landeskirchlichen Identit\xe4t',
  'title': u'Die Evangelisch-Lutherische Kirche in Th\xfcringen in der SBZ und Fr\xfchzeit der DDR (1945-1961)',
  'uri': 'http://www.sehepunkte.de/export/rezension_18240.html',
  'volume': '10',
  'year': '2010'},
 {'authors': [{'firstname': 'Ahlrich', 'lastname': 'Meyer'}],
  'category': 'Zeitgeschichte',
  'isbn': '978-3-506-77023-3',
  'issue': '11',
  'pages': '238',
  'placeOfPublication': 'Paderborn',
  'publisher': u'Ferdinand Sch\xf6ningh',
  'reviewAuthorFirstname': 'Katja',
  'reviewAuthorLastname': 'Happe',
  'series': '',
  'subtitle': u'T\xe4ter und Opfer der "Endl\xf6sung" in Westeuropa',
  'title': 'Das Wissen um Auschwitz',
  'uri': 'http://www.sehepunkte.de/export/rezension_18702.html',
  'volume': '10',
  'year': '2010'},
 {'authors': [{'firstname': 'Stefanie', 'lastname': 'Middendorf'}],
  'category': 'Zeitgeschichte',
  'isbn': '978-3-8353-0542-7',
  'issue': '11',
  'pages': '507',
  'placeOfPublication': u'G\xf6ttingen',
  'publisher': 'Wallstein',
  'reviewAuthorFirstname': 'Dietmar',
  'reviewAuthorLastname': u'H\xfcser',
  'series': 'Moderne Zeit. Neue Forschungen zur Gesellschafts- und Kulturgeschichte des 19. und 20. Jahrhunderts',
  'subtitle': u'Zur Wahrnehmung gesellschaftlicher Modernit\xe4t in Frankreich 1880 - 1980',
  'title': 'Massenkultur',
  'uri': 'http://www.sehepunkte.de/export/rezension_17343.html',
  'volume': '10',
  'year': '2010'},
 {'authors': [{'firstname': 'Bogdan', 'lastname': 'Musial'}],
  'category': 'Zeitgeschichte',
  'isbn': '978-3-549-07370-4',
  'issue': '11',
  'pages': '507',
  'placeOfPublication': u'Berlin / M\xfcnchen',
  'publisher': u'Propyl\xe4en',
  'reviewAuthorFirstname': 'Rainer',
  'reviewAuthorLastname': 'Karlsch',
  'series': '',
  'subtitle': u'Die Pl\xfcnderung Deutschlands und der Aufstieg der Sowjetunion zur Weltmacht',
  'title': 'Stalins Beutezug',
  'uri': 'http://www.sehepunkte.de/export/rezension_18607.html',
  'volume': '10',
  'year': '2010'},
 {'authors': [{'firstname': 'Martin', 'lastname': 'Greschat'}],
  'category': 'Zeitgeschichte',
  'isbn': '978-3-506-76806-3',
  'issue': '11',
  'pages': '454',
  'placeOfPublication': 'Paderborn',
  'publisher': u'Ferdinand Sch\xf6ningh',
  'reviewAuthorFirstname': 'Clemens',
  'reviewAuthorLastname': 'Vollnhals',
  'series': '',
  'subtitle': 'Kirche, Politik und Gesellschaft  im geteilten Deutschland 1945-1963',
  'title': 'Protestantismus im Kalten Krieg',
  'uri': 'http://www.sehepunkte.de/export/rezension_18543.html',
  'volume': '10',
  'year': '2010'},
 {'authors': [{'firstname': 'K. Erik', 'lastname': 'Franzen'}],
  'category': 'Zeitgeschichte',
  'isbn': '978-3-486-59150-7',
  'issue': '11',
  'pages': 'IX + 520',
  'placeOfPublication': u'M\xfcnchen',
  'publisher': 'Oldenbourg',
  'reviewAuthorFirstname': 'Susanne',
  'reviewAuthorLastname': 'Greiter',
  'series': u'Ver\xf6ffentlichungen des Collegium Carolinum',
  'subtitle': u'Die Schirmherrschaft \xfcber die Sudetendeutschen 1954-1974',
  'title': 'Der vierte Stamm Bayerns',
  'uri': 'http://www.sehepunkte.de/export/rezension_18295.html',
  'volume': '10',
  'year': '2010'},
 {'authors': [{'firstname': 'Daniel', 'lastname': 'Lenski'}],
  'category': 'Zeitgeschichte',
  'isbn': '978-3-933816-41-2',
  'issue': '11',
  'pages': '171',
  'placeOfPublication': 'Berlin',
  'publisher': 'Edition Kirchhof & Franke',
  'reviewAuthorFirstname': 'Tim',
  'reviewAuthorLastname': 'Szatkowski',
  'series': '',
  'subtitle': u'Das Amtsverst\xe4ndnis der ersten f\xfcnf Bundespr\xe4sidenten unter besonderer Ber\xfcckichtigung ihrer verfassungsrechtlichen Kompetenzen',
  'title': 'Von Heuss bis Carstens',
  'uri': 'http://www.sehepunkte.de/export/rezension_18207.html',
  'volume': '10',
  'year': '2010'},
 {'authors': [{'firstname': 'Volker', 'lastname': 'Zimmermann'}],
  'category': 'Zeitgeschichte',
  'isbn': '978-3-8375-0296-1',
  'issue': '11',
  'pages': '639',
  'placeOfPublication': 'Essen',
  'publisher': 'Klartext',
  'reviewAuthorFirstname': 'Hermann',
  'reviewAuthorLastname': 'Wentker',
  'series': u'Ver\xf6ffentlichungen zur Kultur und Geschichte im \xf6stlichen Europa',
  'subtitle': 'Die Beziehungen zwischen der SBZ/DDR und der Tschechoslowakei (1945-1969)',
  'title': 'Eine sozialistische Freundschaft im Wandel',
  'uri': 'http://www.sehepunkte.de/export/rezension_18414.html',
  'volume': '10',
  'year': '2010'},
 {'authors': [{'firstname': 'Michael', 'lastname': 'Klinkenberg'}],
  'category': u'Epochen\xfcbergreifend',
  'isbn': '978-3-8253-5585-2',
  'issue': '11',
  'pages': '662',
  'placeOfPublication': 'Heidelberg',
  'publisher': u'Universit\xe4tsverlag Winter',
  'reviewAuthorFirstname': 'Tonia',
  'reviewAuthorLastname': u'Sch\xfcller',
  'series': '',
  'subtitle': '',
  'title': u'Das Orientbild in der franz\xf6sischen Literatur und Malerei vom 17. Jahrhundert bis zum fin de si\xe8cle',
  'uri': 'http://www.sehepunkte.de/export/rezension_17304.html',
  'volume': '10',
  'year': '2010'},
 {'authors': [{'firstname': 'Stephen F.', 'lastname': 'Dale'}],
  'category': u'Epochen\xfcbergreifend',
  'isbn': '978-0-521-69142-0',
  'issue': '11',
  'pages': 'XIV + 347',
  'placeOfPublication': 'Cambridge',
  'publisher': 'Cambridge University Press',
  'reviewAuthorFirstname': 'Tonia',
  'reviewAuthorLastname': u'Sch\xfcller',
  'series': '',
  'subtitle': '',
  'title': 'The Muslim Empires of the Ottomans, Safavids, and Mughals',
  'uri': 'http://www.sehepunkte.de/export/rezension_18550.html',
  'volume': '10',
  'year': '2010'},
 {'authors': [{'firstname': 'Benny', 'lastname': 'Morris'}],
  'category': 'Zeitgeschichte',
  'isbn': '978-0-300-12696-9',
  'issue': '11',
  'pages': 'xiv + 524',
  'placeOfPublication': 'New Haven / London',
  'publisher': 'Yale University Press',
  'reviewAuthorFirstname': 'Wolfgang G.',
  'reviewAuthorLastname': 'Schwanitz',
  'series': '',
  'subtitle': 'A History of the First Arab-Israeli War',
  'title': '1948',
  'uri': 'http://www.sehepunkte.de/export/rezension_14920.html',
  'volume': '10',
  'year': '2010'},
 {'authors': [{'firstname': 'Bettina', 'lastname': u'Gr\xe4f'},
              {'firstname': 'Jakob', 'lastname': 'Skovgaard-Petersen'}],
  'category': u'Epochen\xfcbergreifend',
  'isbn': '978-1-85065-939-6',
  'issue': '11',
  'pages': 'XI + 262',
  'placeOfPublication': 'London',
  'publisher': 'C. Hurst & Co',
  'reviewAuthorFirstname': 'Wolfgang G.',
  'reviewAuthorLastname': 'Schwanitz',
  'series': '',
  'subtitle': 'The Phenomenon of Yusuf al-Qaradawi',
  'title': 'Global Mufti',
  'uri': 'http://www.sehepunkte.de/export/rezension_16198.html',
  'volume': '10',
  'year': '2010'},
 {'authors': [{'firstname': 'Lorenz', 'lastname': 'Korn'},
              {'firstname': 'Eva', 'lastname': 'Orthmann'},
              {'firstname': 'Florian', 'lastname': 'Schwarz'}],
  'category': u'Epochen\xfcbergreifend',
  'isbn': '978-3-89500-675-3',
  'issue': '11',
  'pages': '319',
  'placeOfPublication': 'Wiesbaden',
  'publisher': 'Reichert Verlag',
  'reviewAuthorFirstname': 'Jens',
  'reviewAuthorLastname': 'Scheiner',
  'series': '',
  'subtitle': 'Arabica et Iranica ad honorem Heinz Gaube',
  'title': 'Die Grenzen der Welt',
  'uri': 'http://www.sehepunkte.de/export/rezension_17971.html',
  'volume': '10',
  'year': '2010'},
 {'authors': [{'firstname': 'Stephan', 'lastname': 'Conermann'},
              {'firstname': 'Syrinx von', 'lastname': 'Hees'}],
  'category': u'Epochen\xfcbergreifend',
  'isbn': '978-3-936912-12-8',
  'issue': '11',
  'pages': '382',
  'placeOfPublication': 'Schenefeld',
  'publisher': 'EB-Verlag',
  'reviewAuthorFirstname': 'Assia Maria',
  'reviewAuthorLastname': 'Harwazinski',
  'series': 'Bonner Islamstudien',
  'subtitle': u'Historische Anthropologie. Ans\xe4tze und M\xf6glichkeiten',
  'title': 'Islamwissenschaft als Kulturwissenschaft I',
  'uri': 'http://www.sehepunkte.de/export/rezension_19082.html',
  'volume': '10',
  'year': '2010'},
 {'authors': [{'firstname': 'Angelika', 'lastname': 'Schaser'},
              {'firstname': 'Stefanie',
               'lastname': u'Sch\xfcler-Springorum'}],
  'category': u'Epochen\xfcbergreifend',
  'isbn': '978-3-515-09319-4',
  'issue': '11',
  'pages': '224',
  'placeOfPublication': 'Stuttgart',
  'publisher': 'Franz Steiner Verlag',
  'reviewAuthorFirstname': 'Horst',
  'reviewAuthorLastname': 'Sassin',
  'series': u'Stiftung Bundespr\xe4sident-Theodor-Heuss-Haus. Wissenschaftliche Reihe',
  'subtitle': 'In- und Exklusionsprozesse im Kaiserreich und in der Weimarer Republik',
  'title': 'Liberalismus und Emanzipation',
  'uri': 'http://www.sehepunkte.de/export/rezension_18795.html',
  'volume': '10',
  'year': '2010'},
 {'authors': [{'firstname': 'Hans-Joachim', 'lastname': 'Behr'}],
  'category': '19. Jahrhundert',
  'isbn': '978-3-89710-435-8',
  'issue': '11',
  'pages': '462',
  'placeOfPublication': 'Paderborn',
  'publisher': 'Bonifatius',
  'reviewAuthorFirstname': 'Wilhelm',
  'reviewAuthorLastname': 'Ribhegge',
  'series': u'Studien und Quellen zur westf\xe4lischen Geschichte',
  'subtitle': 'Das Leben des Freiherrn Georg von Vincke (1811-1875)',
  'title': u'"Recht mu\xdf doch Recht bleiben"',
  'uri': 'http://www.sehepunkte.de/export/rezension_18485.html',
  'volume': '10',
  'year': '2010'},
 {'authors': [{'firstname': 'Ina', 'lastname': 'Eichner'},
              {'firstname': 'Vasiliki', 'lastname': 'Tsamakda'}],
  'category': u'Epochen\xfcbergreifend',
  'isbn': '978-3-89500-674-6',
  'issue': '11',
  'pages': 'VIII + 296',
  'placeOfPublication': 'Wiesbaden',
  'publisher': 'Reichert Verlag',
  'reviewAuthorFirstname': 'Jens',
  'reviewAuthorLastname': 'Scheiner',
  'series': u'Sp\xe4tantike - Fr\xfches Christentum - Byzanz. Kunst im ersten Jahrtausend. Reihe B: Studien und Perspektiven',
  'subtitle': '',
  'title': u'Syrien und seine Nachbarn von der Sp\xe4tantike bis in die islamische Zeit',
  'uri': 'http://www.sehepunkte.de/export/rezension_17970.html',
  'volume': '10',
  'year': '2010'},
 {'authors': [{'firstname': 'Klaus', 'lastname': 'Kreiser'}],
  'category': u'Epochen\xfcbergreifend',
  'isbn': '978-3-406-59063-4',
  'issue': '11',
  'pages': '320',
  'placeOfPublication': u'M\xfcnchen',
  'publisher': 'C.H.Beck',
  'reviewAuthorFirstname': 'Tilmann',
  'reviewAuthorLastname': 'Kulke',
  'series': '',
  'subtitle': u'Ein historischer Stadtf\xfchrer',
  'title': 'Istanbul',
  'uri': 'http://www.sehepunkte.de/export/rezension_17429.html',
  'volume': '10',
  'year': '2010'},
 {'authors': [{'firstname': 'Mathias', 'lastname': 'Rohe'}],
  'category': u'Epochen\xfcbergreifend',
  'isbn': '978-3-406-57955-4',
  'issue': '11',
  'pages': 'XV + 606',
  'placeOfPublication': u'M\xfcnchen',
  'publisher': 'C.H.Beck',
  'reviewAuthorFirstname': 'Heidrun',
  'reviewAuthorLastname': 'Eichner',
  'series': '',
  'subtitle': 'Geschichte und Gegenwart',
  'title': 'Das islamische Recht',
  'uri': 'http://www.sehepunkte.de/export/rezension_16363.html',
  'volume': '10',
  'year': '2010'},
 {'authors': [{'firstname': 'Samir', 'lastname': 'Suleiman'}],
  'category': u'Epochen\xfcbergreifend',
  'isbn': '978-3-86858-330-4',
  'issue': '11',
  'pages': '280',
  'placeOfPublication': 'Aachen',
  'publisher': 'Shaker Verlag',
  'reviewAuthorFirstname': 'Tonia',
  'reviewAuthorLastname': u'Sch\xfcller',
  'series': '',
  'subtitle': u'Ein Beitrag zur interkulturellen Verst\xe4ndigung',
  'title': u'Der Islam muss kein R\xe4tsel sein',
  'uri': 'http://www.sehepunkte.de/export/rezension_17982.html',
  'volume': '10',
  'year': '2010'}]


class FakeLogger(object):
    def __init__(self):
        self.reset()

    def reset(self):
        self.errors = []

    def error(self, error):
        self.errors.append(error)

class TestSehepunkteImport(unittest.TestCase):
    def setUp(self):
        self.fake_logger = FakeLogger()
        importSehepunkte.logger = self.fake_logger
        self.originalUrlGetter = sehepunkte_parser._getHTMLData
        sehepunkte_parser._getHTMLData = lambda a:a

    def tearDown(self):
        sehepunkte_parser._getHTMLData = self.originalUrlGetter

    def testImportGood(self):
        should_be = []
        data = [x for x in sehepunkte_parser.parse(file(testdata_filename).read())]
        for dataset in data:
            dataset.pop('html')
        self.assertEquals(testdata_parsed, list(data))

    def testImportBad(self):
        data1 = file(testdata_filename).read()
        data2 = data1.replace('<review id="17542">', '<somethingelse>')
        data2 = data2.replace('</review>', '</somethingelse>', 1)
        data1 = sehepunkte_parser.parse(data1)
        data2 = sehepunkte_parser.parse(data2)
        self.assertEquals(len(list(data1)), len(list(data2)) + 1)

    def testBadURL(self):
        sehepunkte_parser._getHTMLData = self.originalUrlGetter
        data = file(testdata_filename).read()
        data = data.replace('http://www.sehepunkte.de/export/rezension_17542.html', 'http://doesnotexist.syslab.de')
        self.assertRaises(IOError, list, sehepunkte_parser.parse(data))
