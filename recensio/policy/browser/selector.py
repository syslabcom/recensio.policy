from plone.app.layout.navigation.interfaces import INavigationRoot

from Acquisition import aq_chain
from Acquisition import aq_inner
from Products.CMFCore.interfaces import ISiteRoot

from Products.LinguaPlone.interfaces import ITranslatable

from Products.LinguaPlone.browser.selector import TranslatableLanguageSelector
from Products.LinguaPlone.interfaces import ITranslatable


class RecensioLanguageSelector(TranslatableLanguageSelector):
    """ Language selector for translatable content.
        Reason for overwriting: We also have non-LP aware content types.
        For them, we don't want to find the "closest" translation,
        but only append the set_language
    """

    def _translations(self, missing):
        # Figure out the "closest" translation in the parent chain of the
        # context. We stop at both an INavigationRoot or an ISiteRoot to look
        # for translations.
        context = aq_inner(self.context)
        translations = {}
        chain = aq_chain(context)
        for item in chain:
            if ISiteRoot.providedBy(item) or \
                not ITranslatable.providedBy(item):
                # We have a site root, which works as a fallback
                for c in missing:
                    translations[c] = item
                break

            translatable = ITranslatable(item, None)
            if translatable is None:
                continue

            item_trans = item.getTranslations(review_state=False)
            for code, trans in item_trans.items():
                code = str(code)
                if code not in translations:
                    # If we don't yet have a translation for this language
                    # add it and mark it as found
                    translations[code] = trans
                    missing = missing - set((code, ))

            if len(missing) <= 0:
                # We have translations for all
                break
            if INavigationRoot.providedBy(item):
                # Don't break out of the navigation root jail, we assume
                # the INavigationRoot is usually translated into all languages
                for c in missing:
                    translations[c] = item
                break
        return translations
