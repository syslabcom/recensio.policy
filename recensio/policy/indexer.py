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
            if level == 0:
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
                recurseDict(vd, level + 1, cp)

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
    return getSelfAndParents(obj, "ddcPlace")


@indexer(IReview)
def ddcTime(obj):
    return getSelfAndParents(obj, "ddcTime")


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

    subtitle = obj.getSubtitle()
    values.append(subtitle)

    for additional in getattr(obj, "getAdditionalTitles", lambda: [])():
        values.append(additional["title"])
        values.append(additional["subtitle"])

    shortname = obj.getField("shortnameJournal")
    if shortname:
        values.append(str(shortname.getAccessor(obj)()))

    return values


@indexer(IReview)
def isbn(obj):
    isbn = (
        getattr(obj, "getIsbn", lambda: "")() or getattr(obj, "getIssn", lambda: "")()
    )
    isbn = "".join(isbn.split("-"))
    isbn = "".join(isbn.split(" "))
    isbn_online = (
        getattr(obj, "getIsbn_online", lambda: "")()
        or getattr(obj, "getIssn_online", lambda: "")()
    )
    isbn_online = "".join(isbn_online.split("-"))
    isbn_online = "".join(isbn_online.split(" "))
    return [val for val in [isbn, isbn_online] if val]


def get_field_and_ebook_variant(obj, accessor):
    val_regular = getattr(obj, accessor, lambda: "")()
    val_online = getattr(obj, accessor + "Online", lambda: "")()
    return [val for val in [val_regular, val_online] if val]


@indexer(IReview)
def year(obj):
    return get_field_and_ebook_variant(obj, "getYearOfPublication")


@indexer(IReview)
def place(obj):
    places = get_field_and_ebook_variant(obj, "getPlaceOfPublication") + [
        date["place"] for date in getattr(obj, "getDates", lambda: [])()
    ]
    return places


@indexer(IReview)
def publisher(obj):
    return get_field_and_ebook_variant(obj, "getPublisher")
