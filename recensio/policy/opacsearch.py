from zope.testbrowser.browser import Browser
from BeautifulSoup import BeautifulSoup, Comment

def viewPage(br):
    file('/tmp/lala', 'w').write(br.contents)

class OpacSearch(object):
    def __init__(self, url = 'https://opacplus.bsb-muenchen.de'):
        browser = Browser()
        browser.mech_browser.set_handle_robots(False)
        browser.open(url)
        self.browser = browser
        self.url = url

    def getMetadataForISBN(self, isbn):
        br = self.browser
        try:
            br.getControl(name='searchCategories[1]').value=['540']
        except LookupError:
            raise IOError('Can\'t communicate with Server!')
        br.getControl(name='searchString[1]').value=isbn
        br.getControl(name='submitSearch').click()
        soup = BeautifulSoup(br.contents)
        results = soup('table', {'class' : 'data'})[:-1]
        br.open(self.url)
        return map(createResult, results)

opac = OpacSearch()

def createResult(result):
    try:
        subtitle = getString(result('span', {'class' : 'book_subtitle'})[0])
    except IndexError:
        subtitle = None
    try:
        title = getString(result('span', {'class' : 'book_title'})[0])
    except IndexError:
        title = None
    authors = []
    ppy = ''
    pages = []
    ddc = []
    language = ''
    isbn = ''
    location = publisher = year = ''
    for thing1 in result('span', {'class' : 'book_title'}):
        state = 'not started'
        for thing2 in thing1.parent.contents:
            if state == 'not started':
                try:
                    if thing2.name == 'strong':
                        if thing2.text == u'Autor / Hrsg.:':
                            state = 'authors'
                            continue
                        elif thing2.text == 'Ort, Verlag, Jahr:':
                            state = 'ppy'
                            continue
                        elif thing2.text == 'Umfang:':
                            state = 'pages'
                            continue
                        elif thing2.text == 'Sprache:':
                            state = 'language'
                            continue
                        elif thing2.text == 'Schlagwort:':
                            state = 'ddc'
                            continue
                        elif thing2.text == 'ISBN-ISSN-ISMN:':
                            state = 'isbn'
                            continue
                        else:
                            pass
                except AttributeError:
                    pass
            elif state == 'authors':
                try:
                    if thing2.name == 'a':
                        authors.append(thing2.text)
                    elif thing2.name == 'br':
                        state = 'not started'
                        continue
                    else:
                        pass
                except AttributeError:
                    pass
            elif state == 'ddc':
                try:
                    if thing2.name == 'a':
                        ddc.append(thing2.text)
                    elif thing2.name == 'br':
                        state = 'not started'
                        continue
                    else:
                        pass
                except AttributeError:
                    pass
            elif state == 'ppy':
                try:
                    if thing2.name == 'br':
                        if ppy.count(',') == 2:
                            location, publisher, year = ppy.split(',')
                        else:
                            publisher = ppy
                        location = location.strip()
                        publisher = publisher.strip()
                        year = year.strip()
                        state = 'not started'
                        continue
                except AttributeError:
                    ppy += unicode(thing2)
            elif state == 'pages':
                try:
                    if thing2.name == 'br':
                        if len(pages) == 1:
                            pages = str(pages[0])
                        elif not len(pages):
                            pages = None
                        else:
                            pages = ' '.join([str(x) for x in pages])
                        state = 'not started'
                        continue
                except AttributeError:
                    try:
                        for bit in unicode(thing2).split():
                            pages.append(int(bit))
                    except ValueError:
                        pass
            elif state == 'language':
                try:
                    if thing2.name == 'br':
                        state = 'not started'
                        continue
                except AttributeError:
                    language += thing2
            elif state == 'isbn':
                try:
                    if thing2.name == 'br':
                        state = 'not started'
                        continue
                except AttributeError:
                    isbn += unicode(thing2)
            else:
                raise AttributeError("Unknown state! %s" % state)
    def makeAuthors(raw):
        if raw.count(',') == 1:
            lastname, firstname = raw.split(',')
            lastname, firstname = map(unicode.strip, (lastname, firstname))
        else:
            firstname = None
            lastname = raw.strip()
        return {'firstname' : firstname, 'lastname' : lastname}
    authors = map(makeAuthors, list(set(authors)))
    authors.sort()

    title = title and title.strip() or None
    subtitle = subtitle and subtitle.strip() or None
    language = language and language.strip() or None
    isbn = isbn and isbn.strip() or None
    pages = pages and pages or None
    location = location and location or None
    publisher = publisher and publisher or None
    year = year and year or None
    ddc = ddc and ddc or None

    return {'title' : title
           ,'subtitle' : subtitle
           ,'authors' : authors
           ,'language' : language
           ,'isbn' : isbn
           ,'ddc' : ddc
           ,'location' : location
           ,'publisher' : publisher
           ,'pages' : pages
           ,'year' : year
           }

def getString(soup):
    if hasattr(soup, 'contents'):
        return ''.join(map(getString, soup.contents))
    else:
        if not isinstance(soup, Comment):
            return unicode(soup)
        else:
            return u''
