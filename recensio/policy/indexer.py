from zope.interface import Interface
from plone.indexer.decorator import indexer
from Products.CMFCore.utils import getToolByName
from plone.memoize import ram
from recensio.contenttypes.interfaces.review import IReview

def _getParentsMap_cachekey(method, obj, vocab):
    return (vocab,)

@ram.cache(_getParentsMap_cachekey)
def getParentsMap(obj, vocab):
    # get the complete dictionary
    vd = vocab.getVocabularyDict(obj)

    # the mapping holds a list of parent ids for every term id
    parents_map = dict()

    def recurseDict(vocab_dict, level, cp):
        for k in vocab_dict.keys():
            # clear the list of current parents for top level nodes
            if level==0:
                cp = list()
            else:
                # if it is not a root node, prune the list of current parents
                #  ( it cannot be longer than the current level )
                cp = cp[:level]
                # and add the parents to the mapping
                parents_map[k] = [x for x in cp]
            vd = vocab_dict[k][1]
            if vd:
                # recurse one level deeper
                cp.append(k)
                recurseDict(vd, level+1, cp)
    recurseDict(vd, 0, list())
    return parents_map


def getSelfAndParents(obj, name):
    field = obj.getField(name)
    if not field:
        return []

    termUID = field.getRaw(obj)
    vocab = field.vocabulary
    
    parents_map = getParentsMap(obj, vocab)
    res = set()
    for term in termUID:
        res.update(parents_map.get(term, []) + [term])

    return list(res)


@indexer(Interface)
def ddcPlace(obj):
    return getSelfAndParents(obj, 'ddcPlace')

@indexer(IReview)
def ddcTime(obj):
    return getSelfAndParents(obj, 'ddcTime')

@indexer(IReview)
def authorsFulltext(obj):
    return obj.getAllAuthorDataFulltext()

@indexer(IReview)
def authors(obj):
    return obj.getAllAuthorData()

@indexer(IReview)
def titleOrShortname(obj):
    values = []
    
    title = str(obj.Title())
    values.append(title)

    shortname = obj.getField('shortnameJournal')
    if shortname:
        values.append(str(shortname.getAccessor(obj)()))

    return values
    
@indexer(IReview)
def isbn(obj):
    isbn = getattr(obj, 'getIsbn', lambda:'')() or getattr(obj, 'getIssn', lambda:'')()
    isbn = ''.join(isbn.split('-'))
    isbn = ''.join(isbn.split(' '))
    return isbn
