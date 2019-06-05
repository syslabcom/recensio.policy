from zope.testbrowser.browser import Browser
from mechanize._mechanize import LinkNotFoundError
from BeautifulSoup import BeautifulSoup, Comment
import re

def viewPage(br):
    file('/tmp/lala', 'w').write(br.contents)

class OpacSearch(object):
    def __init__(self, url = 'http://opac.bib-bvb.de:8080/InfoGuideClient.fasttestsis/search.do?methodToCall=switchSearchPage&SearchType=2'):
        browser = Browser()
        browser.mech_browser.set_handle_robots(False)
        browser.open(url)
        self.browser = browser
        self.url = url

    def getMetadataForISBN(self, isbn):
        br = self.browser
        try:
            br.getControl(name='searchCategories[0]').value=['540']
        except LookupError:
            try:
                br.getLink('Neu starten').click()
                br.getLink('Erweiterte Suche').click()
                br.getControl(name='searchCategories[0]').value=['540']
            except (LinkNotFoundError, LookupError):
                raise IOError('Can\'t communicate with Server!')
        br.getControl(name='searchString[0]').value=isbn
        br.getForm().submit()
        soup = BeautifulSoup(br.contents)
        try:
            results = soup('table', {'class' : 'data'})[0].findAll('tr')
        except:
            try:
                results = []
                base_url = '/'.join(br.url.split('/')[:3])
                for result in soup('table', {'class' : 'data kurztrefferliste'})[0].findAll('tr'):
                    br.open(base_url + result.findAll('a')[3]['href'])
                    soup = BeautifulSoup(br.contents)
                    results.extend(soup('table', {'class' : 'data'})[0].findAll('tr'))
            except:
                br.open(self.url)
                return []
        br.open(self.url)
        return map(createResult, results)

# The default URL for OpacSearch times out. Instantiating at module level
# blocks everything that refers to this module.
#opac = OpacSearch()
opac = None

def createResult(result):
    raw_stuff = {}
    key = None
    try:
        stuff = result.td.contents
    except:
        stuff = []
    for thing in stuff:
        try:
            if thing.name == 'strong':
                key = getString(thing)
                raw_stuff[key] = ''
                continue
        except AttributeError:
            pass
        if getString(thing) not in ['', '\n'] and key:
            raw_stuff[key] += getString(thing)
    authors = []
    for author_field in [raw_stuff.get(x, '') for x in 'Verfasser:', 
                                                        'Autor/Person:']:
        for author in author_field.split(';'):
            if not author:
                continue
            if author.count(',') == 1:
                lastname, firstname = author.split(',')
                lastname, firstname = map(unicode.strip, (lastname, firstname))
            else:
                firstname = None
                lastname = author.strip()
            authors.append({'firstname' : firstname, 'lastname' : lastname})
    title = raw_stuff.get('Titel:', '').split('|')[0].strip().replace(u'\xac', '')
    subtitle = ("|".join([x.strip() for x in raw_stuff.get('Titel:', '').split('|')[1:]])).replace(u'\xac', '')
    language = raw_stuff.get('Sprache:', '')
    isbn = raw_stuff.get('ISBN/ISMN:', '')
    try:
        pages = ''.join([(x in '1234567890' and x) or ' ' for x in raw_stuff.get('Impressum:', '').split(':')[3].strip()]).strip().split()[0]
    except:
        pages = u''
    try:
        location = raw_stuff.get('Impressum:', '').split(':')[0].strip()
    except:
        location = u''
    try:
        publisher = raw_stuff.get('Impressum:', '').split(':')[1].strip()
    except:
        publisher = u''
    try:
        year = raw_stuff.get('Impressum:', '').split(':')[2].strip()
    except:
        year = u''
    ddc = list(set(re.compile('[GSZ][: ][^, ]*').findall(raw_stuff.get('Notation:', ''))))
    keywords = set()
    for key in filter(lambda x:x.startswith('Schlagw'), raw_stuff.keys()):
       for keyword in raw_stuff.get(key, '').split(';'):
             keywords.add(keyword.strip())
    keywords = list(keywords)

    return {'title' : title or None
           ,'subtitle' : subtitle or None
           ,'authors' : authors or []
           ,'language' : language or None
           ,'isbn' : isbn or None
           ,'ddc' : ddc or None
           ,'location' : location or None
           ,'keywords' : keywords or []
           ,'publisher' : publisher or None
           ,'pages' : pages or None
           ,'year' : year or None
           }

def getString(soup):
    if hasattr(soup, 'contents'):
        subcontents = []
        for content in soup.contents:
            if hasattr(content, 'name') and content.name == u'br':
                break
            else:
                subcontents.append(content)
        return ''.join(map(getString, subcontents))
    else:
        if not isinstance(soup, Comment):
            return unicode(soup).replace('&nbsp;', ' ').replace('&lt;', '<').replace('&gt;', '>').strip()
        else:
            return u''
