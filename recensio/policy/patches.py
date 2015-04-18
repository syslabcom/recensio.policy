from collective.solr import indexer, mangler
#from collective.solr.indexer import datehandler
from collective.solr.mangler import *
from Products.CMFPlone.utils import safe_unicode

# This seems to be fixed with Solr 3.3, but keep an eye out for problems!

#def inthandler(value):
    # solr would choke on None and throw a javalangNumberFormatException,
    # preventing the whole object from being indexed. Therefore raise an
    # AttributeError in this case.
#    if value is None:
#        raise AttributeError
#    return value

#indexer.handlers = {
#    'solr.DateField': datehandler,
#    'solr.TrieDateField': datehandler,
#    'solr.IntField': inthandler,
#    'solr.TrieIntField': inthandler,
#}

def mangleQuery(keywords, config, schema):
    """ translate / mangle query parameters to replace zope specifics
        with equivalent constructs for solr """
    extras = {}
    for key, value in keywords.items():
        value = safe_unicode(value)
        if key.endswith('_usage'):          # convert old-style parameters
            category, spec = value.split(':', 1)
            extras[key[:-6]] = {category: spec}
            del keywords[key]
        elif isinstance(value, dict):       # unify dict parameters
            keywords[key] = value['query']
            del value['query']
            extras[key] = value
        elif hasattr(value, 'query'):       # unify object parameters
            keywords[key] = value.query
            extra = dict()
            for arg in query_args:
                arg_val = getattr(value, arg, None)
                if arg_val is not None:
                    extra[arg] = arg_val
            extras[key] = extra
        elif key in ignored:
            del keywords[key]

    # find EPI indexes
    if schema:
        epi_indexes = {}
        for name in schema.keys():
            parts = name.split('_')
            if parts[-1] in ['string', 'depth', 'parents']:
                count = epi_indexes.get(parts[0], 0)
                epi_indexes[parts[0]] = count + 1
        epi_indexes = [k for k, v in epi_indexes.items() if v == 3]
    else:
        epi_indexes = ['path']

    for key, value in keywords.items():
        value = safe_unicode(value)
        args = extras.get(key, {})
        if key == 'SearchableText':
            pattern = getattr(config, 'search_pattern', '')
            simple_term = isSimpleTerm(value)
            if pattern and isSimpleSearch(value):
                base_value = value
                if simple_term:             # use prefix/wildcard search
                    value = u'(%s* OR %s)' % (value.lower(), value)
                elif isWildCard(value):     # wildcard searches need lower-case
                    value = value.lower()
                    base_value = safe_unicode(quote(value.replace('*', '').replace('?', '')))
                # simple queries use custom search pattern
                value = safe_unicode(pattern.format(value=quote(value),
                                     base_value=quote(value))).encode('utf8')
                keywords[key] = set([value])    # add literal query parameter
                continue
            elif simple_term:               # use prefix/wildcard search
                keywords[key] = u'(%s* OR %s)' % (value.lower(), value)
                continue
        if key in epi_indexes:
            path = keywords['%s_parents' % key] = value
            del keywords[key]
            if 'depth' in args:
                depth = int(args['depth'])
                if depth >= 0:
                    if not isinstance(value, (list, tuple)):
                        path = [path]
                    tmpl = '(+%s_depth:[%d TO %d] AND +%s_parents:%s)'
                    params = keywords['%s_parents' % key] = set()
                    for p in path:
                        base = len(p.split('/'))
                        params.add(tmpl % (key, base + (depth and 1), base + depth, key, p))
                del args['depth']
        elif key == 'effectiveRange':
            if isinstance(value, DateTime):
                steps = getattr(config, 'effective_steps', 1)
                if steps > 1:
                    value = DateTime(value.timeTime() // steps * steps)
                value = iso8601date(value)
            del keywords[key]
            keywords['effective'] = '[* TO %s]' % value
            keywords['expires'] = '[%s TO *]' % value
        elif key == 'show_inactive':
            del keywords[key]           # marker for `effectiveRange`
        elif 'range' in args:
            if not isinstance(value, (list, tuple)):
                value = [value]
            payload = map(iso8601date, value)
            keywords[key] = ranges[args['range']] % tuple(payload)
            del args['range']
        elif 'operator' in args:
            if isinstance(value, (list, tuple)) and len(value) > 1:
                sep = ' %s ' % args['operator'].upper()
                value = sep.join(
                    [u'"%s"' % x for x in map(safe_unicode, map(iso8601date, value))]
                ).encode('utf-8')
                keywords[key] = '(%s)' % value
            del args['operator']
        elif key == 'allowedRolesAndUsers':
            if getattr(config, 'exclude_user', False):
                token = 'user$' + getSecurityManager().getUser().getId()
                if token in value:
                    value.remove(token)
        elif isinstance(value, DateTime):
            keywords[key] = iso8601date(value)
        elif not isinstance(value, basestring):
            assert not args, 'unsupported usage: %r' % args


mangler.mangleQuery = mangleQuery

def patch(old_method):
    def contentIndependentGetVocabularyDict(self, instance=None):
        return old_method(self)
    return contentIndependentGetVocabularyDict

try:
    from Products.CMFCore.utils import getToolByName
    from Products.ATVocabularyManager.config import SORT_METHOD_LEXICO_VALUES

    def patch2(old_method):
        def getSortedKeysCheckLang(self):
            sortMethod = self.getSortMethod()
            if sortMethod == SORT_METHOD_LEXICO_VALUES:
                langtool = getToolByName(self,'portal_languages')
                lang = langtool.getPreferredLanguage()
                terms = self.contentValues()
                terms.sort(lambda x,y:cmp(x.getTermValue(lang),y.getTermValue(lang)))
                return [term.getVocabularyKey() for term in terms]
            else:
                return old_method(self)
        return getSortedKeysCheckLang

    from Products.ATVocabularyManager.types import tree, simple

    tree_voc = tree.vocabulary.TreeVocabulary

    tree_voc.getVocabularyDict = patch(tree_voc.getVocabularyDict)
    tree_voc.getSortedKeys = patch2(tree_voc.getSortedKeys)

    simple_voc = simple.vocabulary.SimpleVocabulary

    simple_voc.getVocabularyDict = patch(simple_voc.getVocabularyDict)
    simple_voc.getSortedKeys = patch2(simple_voc.getSortedKeys)

except ImportError:
    pass
