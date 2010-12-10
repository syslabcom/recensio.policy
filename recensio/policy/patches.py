from collective.solr.flare import PloneFlare
from collective.solr import indexer, mangler
from collective.solr.indexer import datehandler
from collective.solr.mangler import mangleQuery as mangleQuerySolr

def getRID(self):
    """ Return a Resource Identifier, like a brain would do """
    return self.UID 

PloneFlare.getRID = getRID

PloneFlare._unrestrictedGetObject = PloneFlare.getObject

def inthandler(value):
    # solr would choke on None and throw a javalangNumberFormatException,
    # preventing the whole object from being indexed. Therefore raise an
    # AttributeError in this case.
    if value is None:
        raise AttributeError
    return value

indexer.handlers = {
    'solr.DateField': datehandler,
    'solr.TrieDateField': datehandler,
    'solr.IntField': inthandler,
    'solr.TrieIntField': inthandler,
}

def mangleQuery(keywords):
    """ patch solr's mangler to behave like standard catalog with path-depth queries
    """
    path = ''
    depth = ''
    if 'path' in keywords.keys():
        if isinstance(keywords['path'], dict):
            path = keywords['path']['query']
            if 'depth' in keywords['path'].keys():
                depth = int(keywords['path']['depth'])
    if path and depth and depth >= 0:
        if not isinstance(path, (list, tuple)):
            path = [path]
        tmpl = '(+physicalDepth:[%d TO %d] AND +parentPaths:%s)'
        params = set()
        for p in path:
            base = len(p.split('/'))
            mangleQuerySolr(keywords)
            keywords['parentPaths'].remove(tmpl % (base, base + depth, p))
            keywords['parentPaths'].add(tmpl % (base + (depth and 1), base + depth, p))

mangler.mangleQuery = mangleQuery
