from lxml import etree

import urllib

class SehepunkteParser(object):
    def parse(self, data):
        root = etree.fromstring(data)
        global_data = self._getGlobalData(root)
        for review in root:
            review_data = self._getReviewData(review)
            if not review_data:
                continue
            review_data.update(global_data)
            yield review_data

    def _getGlobalData(self, elem):
        return {
            'issue' : elem.get('number')
           ,'volume' : elem.get('volume')
           ,'year'   : elem.get('year')

        }

    def _getReviewData(self, root):
        if root.tag != 'review':
            logger.error('This XML Format seems to be unclean, it contained an unknown element after the issue tag')
            return {}
        xpath_single = lambda x:''.join(root.xpath(x)).strip()

        authors = []
        for i in range(1,4):
            authors.append({
                'lastname'  : xpath_single('book/author_%i_last_name/text()' % i)
               ,'firstname' : xpath_single('book/author_%i_first_name/text()' % i)
            })
        authors = filter(lambda x: x['lastname'] or x['firstname'], authors)

        canonical_uri= xpath_single('filename/text()')

        return {
            'category' : xpath_single('category/text()')
           ,'reviewAuthorLastname' : xpath_single('reviewer/last_name/text()')
           ,'reviewAuthorFirstname' : xpath_single('reviewer/first_name/text()')
           ,'authors' : authors
           ,'isbn' : xpath_single('book/isbn/text()')
           ,'title' : xpath_single('book/title/text()')
           ,'subtitle' : xpath_single('book/subtitle/text()')
           ,'placeOfPublication' : xpath_single('book/place_of_publication/text()')
           ,'publisher' : xpath_single('book/publishing_company/text()')
           ,'yearOfPublication' : xpath_single('book/year/text()')
           ,'series' : xpath_single('book/series/text()')
           ,'pages' : xpath_single('book/pages/text()')
           ,'canonical_uri' : canonical_uri
        }

sehepunkte_parser = SehepunkteParser()
