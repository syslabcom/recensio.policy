from lxml import etree
from datetime import datetime

ns = {'oai' : 'http://www.openarchives.org/OAI/2.0/'\
     ,'oaidc' : 'http://www.openarchives.org/OAI/2.0/oai_dc/'\
     ,'dc' : 'http://purl.org/dc/elements/1.1/'}

xp = lambda x: lambda y:x.xpath(y, namespaces = ns)

class PerspektiviaParser(object):
    def parse(self, data):
        books = []
        reviews = []
        for record in self._deserialize(data):
            if record['type'] == 'Review':
                reviews.append(record)
            elif record['type'] == 'Book':
                books.append(record)
            else:
                raise TypeError('What is type %s in OAI?' % record['type'])
        return {'books' : books, 'reviews' : reviews}

    def _deserialize(self, data):
        root = etree.fromstring(data)
        for element in xp(root)('oai:ListRecords/oai:record'):
            yield self._parseRecord(element)

    def _parseRecord(self, element):
        x = xp(element)
        dc = lambda y: x('oai:metadata/oaidc:dc/dc:%s/text()' % y)
        date = lambda x: datetime.strptime(x, '%Y-%m-%d')
        space = lambda x: ' '.join(dc(x))
        no_space = lambda x: ''.join(dc(x))

        return {
            'id'         : ''.join(x('oai:header/oai:identifier/text()'))
           ,'title'      : space('title')
           ,'creator'    : list(self._creators(*dc('creator')))
           ,'subject'    : space('subject')
           ,'publisher'  : space('publisher')
           ,'date'       : date(no_space('date')) # XXX What is date for?
           ,'type'       : no_space('type')
           ,'format'     : no_space('format') # XXX Alyaws assume html?
           ,'identifier' : no_space('identifier')
           ,'source'     : no_space('source') # XXX Zitierweise?
           ,'rights'     : no_space('rights') # always assume X?
           ,'relation'   : no_space('relation')
        }

    def _creators(self, *creators):
        for creator in creators:
            lastname = creator
            firstname = ''
            if creator.count(',') == 1:
                lastname, firstname = map(lambda x:x.strip(), creator.split(','))
            yield {'firstname' : firstname, 'lastname' : lastname}

perspektivia_parser = PerspektiviaParser()
