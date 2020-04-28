from marcxml_parser.record import record_iterator
from Products.CMFPlone.utils import safe_unicode
from HTMLParser import HTMLParser
import pycountry
import requests
import logging

log = logging.getLogger(__name__)


class MetadataConverter(object):

    keyword_fields = [600, 610, 611, 630, 648, 650, 651, 655]

    def __init__(self, raw, isbn):
        self.records = record_iterator(raw)
        self.isbn = isbn
        self.html_parser = HTMLParser()

    def clean_text(self, value):
        if not value:
            return value
        return self.html_parser.unescape(safe_unicode(value))

    def get_field_as_text(self, fieldspec):
        return safe_unicode(self.clean_text("".join(self.current[fieldspec])))

    def get_field_as_list(self, fieldspec):
        return [self.clean_text(a) for a in self.current[fieldspec]]

    def get_names(self, fieldspec):
        names = []
        for fullname in self.current[fieldspec]:
            lastname, firstname = fullname.split(", ")
            names.append(
                {
                    "lastname": lastname.decode("utf-8"),
                    "firstname": firstname.decode("utf-8"),
                }
            )
        return names

    def get_authors(self):
        return self.get_names("100a")

    def get_editors(self):
        return self.get_names("700a")

    def convertLanguage(self, lang):
        try:
            pylang = pycountry.languages.lookup(lang)
        except LookupError:
            return lang
        return pylang.name

    def get_series(self):
        series_num = self.current.get_part_name()
        series_title = self.get_field_as_text("490a")
        parts = [part for part in [series_num, series_title] if part]
        if parts:
            return self.clean_text("; ".join(parts))
        return ""

    def get_keywords(self):
        keywords = set()
        for field_num in self.keyword_fields:
            value = self.current["{}a".format(field_num)]
            for kw in value:
                if kw:
                    keywords.add(safe_unicode(self.html_parser.unescape(kw)))
        return list(keywords)

    def get_isbn(self):
        isbn = self.isbn.replace("-", "")
        isbns = [i.replace("-", "") for i in self.current.get_ISBNs()]
        if isbn in isbns:
            return isbn
        # The given isbn is not in the record but we have a match anyway.
        # This apparently happens when a review of a work with the given ISBN
        # is returned as a result.
        if not isbns:
            return ""
        return isbns[0]

    def get_ppn(self):
        values = self.current["035a"]
        for value in values:
            value = self.clean_text(value)
            if value.startswith("(DE-627)"):
                return value.replace("(DE-627)", "")
        return ""

    def convert_current(self):
        converted = {
            "title": self.get_field_as_text("245a"),
            "subtitle": self.get_field_as_text("245b"),
            "authors": self.get_authors(),
            "editors": self.get_editors(),
            "language": self.convertLanguage(self.current["008"][35:38]),
            "isbn": self.clean_text(self.get_isbn()),
            "ddcPlace": self.get_field_as_list("082g"),
            "ddcSubject": self.get_field_as_list("082a"),
            "ddcTime": self.get_field_as_list("082f"),
            "location": self.clean_text(
                ", ".join(
                    set(
                        [
                            place
                            for place in self.current["260a  "] + self.current["264a"]
                        ]
                    )
                )
            ),
            "keywords": self.get_keywords(),
            "publisher": self.clean_text(self.current.get_publisher("")),
            "pages": self.get_field_as_text("300a"),
            "series": self.get_series(),
            "seriesVol": self.get_field_as_text("490v"),
            "year": self.clean_text(self.current.get_pub_date("")),
            "bv": self.clean_text(self.current["001"]),
            "ppn": self.get_ppn(),
        }
        return converted

    def convert(self):
        out = []
        for record in self.records:
            self.current = record
            out.append(self.convert_current())
        return out


def fetchMetadata(isbn, base_url, params):
    try:
        response = requests.get(base_url, params=params)
    except requests.exceptions.RequestException as e:
        log.exception(e)
        log.warn("Could not get metadata from {}".format(base_url))
        return None
    return response.content


def getMetadata(isbn):
    sources = [
        {
            "title": "B3Kat",
            "base_url": "http://bvbr.bib-bvb.de:5661/bvb01sru",
            "query": "marcxml.isbn={isbn}".format(isbn=isbn),
            "frontend_url": "http://lod.b3kat.de/page/isbn/",
            "skip": [],
        },
        {
            "title": "SWB",
            "base_url": "http://swb.bsz-bw.de/sru/DB=2.1/username=/password=/",
            "query": "pica.isb={isbn}".format(isbn=isbn),
            "frontend_url": "http://swb.bsz-bw.de/DB=2.1/SET=2/TTL=1/CMD?ACT=SRCHA&IKT=1007&SRT=RLV&MATCFILTER=N&MATCSET=N&NOABS=Y&TRM=",
            "skip": ["bv",],
        },
    ]
    base_params = {
        "version": "1.1",
        "recordSchema": "marcxml",
        "operation": "searchRetrieve",
        "maximumRecords": "6",
    }

    results = []
    for source in sources:
        params = base_params.copy()
        params["query"] = source["query"]
        raw = fetchMetadata(isbn, source["base_url"], params)
        if not raw:
            continue
        source_results = MetadataConverter(raw, isbn).convert()
        for result in source_results:
            result["source"] = {
                "title": source["title"],
                "url": source["frontend_url"] + isbn,
            }
            for field in source["skip"]:
                del result[field]
        results.extend(source_results)
    return results
