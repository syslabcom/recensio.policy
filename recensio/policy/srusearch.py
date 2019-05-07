from marcxml_parser.record import record_iterator
from Products.CMFPlone.utils import safe_unicode
from HTMLParser import HTMLParser
import pycountry
import requests


class MetadataConverter(object):

    keyword_fields = [600, 610, 611, 630, 648, 650, 651, 655]

    def __init__(self, raw, isbn):
        self.records = record_iterator(raw)
        self.isbn = isbn
        self.html_parser = HTMLParser()

    def clean_text(self, value):
        if not value:
            return value
        return safe_unicode(self.html_parser.unescape(value))

    def get_field_as_text(self, fieldspec):
        return self.clean_text(
            u''.join(self.current[fieldspec])
        )

    def get_field_as_list(self, fieldspec):
        return [self.clean_text(a) for a in self.current[fieldspec]]

    def get_authors(self):
        authors = []
        for author in self.current['100a']:  # XXX + self.current['700a']:
            lastname, firstname = author.split(', ')
            authors.append(
                {
                    'lastname': lastname,
                    'firstname': firstname,
                }
            )
        return authors

    def convertLanguage(self, lang):
        try:
            pylang = pycountry.languages.lookup(lang)
        except LookupError:
            return lang
        return pylang.name

    def get_series(self):
        series_num = self.current.get_part_name()
        series_title = self.get_field_as_text('490a')
        parts = [part for part in [series_num, series_title] if part]
        if parts:
            return self.clean_text('; '.join(parts))
        return ''

    def get_keywords(self):
        keywords = set()
        for field_num in self.keyword_fields:
            value = self.current['{}a'.format(field_num)]
            for kw in value:
                if kw:
                    keywords.add(
                        safe_unicode(
                            self.html_parser.unescape(kw)
                        )
                    )
        return list(keywords)

    def get_isbn(self):
        isbn = self.isbn.replace('-', '')
        isbns = [i.replace('-', '') for i in self.current.get_ISBNs()]
        if isbn in isbns:
            return isbn
        # If the given isbn is not in the record then it shouldn't be a match.
        # This should not really happen.
        return isbns[0]

    def convert_current(self):
        converted = {
            'title': self.get_field_as_text('245a'),
            'subtitle': self.get_field_as_text('245b'),
            'authors': self.get_authors(),
            # XXX editors?
            'language': self.convertLanguage(self.current['008'][35:38]),
            'isbn': self.clean_text(self.get_isbn()),
            'ddcPlace': self.get_field_as_list('082g'),
            'ddcSubject': self.get_field_as_list('082a'),
            'ddcTime': self.get_field_as_list('082f'),
            'location': self.clean_text(u', '.join(set(
                [place for place in self.current['260a  '] + self.current['264a']]
            ))),
            'keywords': self.get_keywords(),
            'publisher': self.clean_text(self.current.get_publisher('')),
            'pages': self.get_field_as_text('300a'),
            'series': self.get_series(),
            'seriesVol': self.get_field_as_text('490v'),
            'year': self.clean_text(self.current.get_pub_date('')),
            'bv': self.clean_text(self.current['001']),
        }
        return converted

    def convert(self):
        out = []
        for record in self.records:
            self.current = record
            out.append(self.convert_current())
        return out


def fetchMetadata(isbn):
    base_url = 'http://bvbr.bib-bvb.de:5661/bvb01sru'
    params = {
        'version': '1.1',
        'recordSchema': 'marcxml',
        'operation': 'searchRetrieve',
        'query': 'marcxml.isbn={isbn}'.format(isbn=isbn),
        'maximumRecords': '6',
    }
    response = requests.get(base_url, params=params)
    return response.text


def getMetadata(isbn):
    raw = fetchMetadata(isbn)
    return MetadataConverter(raw, isbn).convert()
