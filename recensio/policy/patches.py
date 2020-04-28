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
                langtool = getToolByName(self, "portal_languages")
                lang = langtool.getPreferredLanguage()
                terms = self.contentValues()
                terms.sort(lambda x, y: cmp(x.getTermValue(lang), y.getTermValue(lang)))
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


def readFromStream(stream):
    name = stream.read(1)
    if name != "/":
        raise utils.PdfReadError, "name read error"
    while True:
        tok = stream.read(1)
        if tok.isspace() or tok in NameObject.delimiterCharacters or tok == "":
            stream.seek(-1, 1)
            break
        name += tok
    return NameObject(name)


from pyPdf.generic import NameObject

NameObject.readFromStream = staticmethod(readFromStream)
