from datetime import datetime

from lxml import etree

ns = {
    "oai": "http://www.openarchives.org/OAI/2.0/",
    "oaidc": "http://www.openarchives.org/OAI/2.0/oai_dc/",
    "dc": "http://purl.org/dc/elements/1.1/",
}

xp = lambda x: lambda y: x.xpath(y, namespaces=ns)


class PerspektiviaParser(object):
    def parse(self, data):
        books = []
        reviews = []
        for record in self._deserialize(data):
            if record["type"] == "Review":
                reviews.append(record)
            elif record["type"] == "Book":
                books.append(record)
            elif record["type"] == "Book(psjBook)":
                record["type"] = "Book"
                books.append(record)
            elif record["type"] == "Review(psjReview)":
                record["type"] = "Review"
                reviews.append(record)
            else:
                raise TypeError("What is type %s in OAI?" % record["type"])
        return {"books": books, "reviews": reviews}

    def _deserialize(self, data):
        root = etree.fromstring(data)
        for element in xp(root)("oai:ListRecords/oai:record"):
            for record in self._parseRecords(element):
                yield record

    def _parseDate(self, date):
        try:
            return datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            return datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ")

    def _parseRecords(self, element):
        x = xp(element)
        dc = lambda y: x("oai:metadata/oaidc:dc/dc:%s/text()" % y)
        space = lambda x: u" ".join(dc(x))
        no_space = lambda x: u"".join(dc(x))

        relations = dc("relation")

        for relation in relations or [""]:

            yield {
                "id": "".join(x("oai:header/oai:identifier/text()")),
                "title": space("title"),
                "creator": list(self._creators(*dc("creator"))),
                "subject": [unicode(subject) for subject in dc("subject")],
                "publisher": space("publisher"),
                "date": self._parseDate(no_space("date")),  # XXX What is date for?
                "type": no_space("type"),
                "format": no_space("format"),  # XXX Alyaws assume html?
                "identifier": no_space("identifier"),
                "source": no_space("source"),  # XXX Zitierweise?
                "rights": no_space("rights"),  # always assume X?
                "relation": unicode(relation),
            }

    def _creators(self, *creators):
        for creator in creators:
            lastname = creator
            firstname = ""
            if creator.count(",") == 1:
                lastname, firstname = map(lambda x: x.strip(), creator.split(","))
            yield {"firstname": unicode(firstname), "lastname": unicode(lastname)}


perspektivia_parser = PerspektiviaParser()
