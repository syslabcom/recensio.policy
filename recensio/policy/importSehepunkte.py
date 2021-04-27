from lxml import etree

import urllib


class NoReview(Exception):
    pass


class SehepunkteParser(object):
    def parse(self, data):
        root = etree.fromstring(data)
        global_data = self._getGlobalData(root)
        for review in root:
            try:
                review_data = self._getReviewData(review)
            except NoReview:
                continue
            review_data.update(global_data)
            for book in review.xpath("book"):
                book_data = self._getBookData(book)
                book_data.update(review_data)
                yield book_data

    def _getGlobalData(self, elem):
        return {
            "issue": elem.get("number"),
            "volume": elem.get("volume"),
            "year": elem.get("year"),
        }

    def _getReviewData(self, root):
        if root.tag != "review":
            logger.error(
                "This XML Format seems to be unclean, it contained an "
                "unknown element after the issue tag"
            )
            raise NoReview()
        xpath_single = lambda x: "".join(root.xpath(x)).strip()

        canonical_uri = xpath_single("filename/text()")

        return {
            "category": xpath_single("category/text()"),
            "reviewAuthors": [
                {
                    "lastname": xpath_single("reviewer/last_name/text()"),
                    "firstname": xpath_single("reviewer/first_name/text()"),
                }
            ],
            "canonical_uri": canonical_uri,
        }

    def _getBookData(self, root):
        xpath_single = lambda x: "".join(root.xpath(x)).strip()

        authors = []
        for i in range(1, 4):
            authors.append(
                {
                    "lastname": xpath_single("author_%i_last_name/text()" % i),
                    "firstname": xpath_single("author_%i_first_name/text()" % i),
                }
            )
        authors = filter(lambda x: x["lastname"] or x["firstname"], authors)

        canonical_uri = xpath_single("filename/text()")

        return {
            "authors": authors,
            "isbn": xpath_single("isbn/text()"),
            "title": xpath_single("title/text()"),
            "subtitle": xpath_single("subtitle/text()"),
            "placeOfPublication": xpath_single("place_of_publication/text()"),
            "publisher": xpath_single("publishing_company/text()"),
            "yearOfPublication": xpath_single("year/text()"),
            "series": xpath_single("series/text()"),
            "pages": xpath_single("pages/text()"),
        }


sehepunkte_parser = SehepunkteParser()
