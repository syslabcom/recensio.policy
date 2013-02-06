from plone.app.layout.navigation.interfaces import INavigationRoot

from Acquisition import aq_chain
from Acquisition import aq_inner
from Products.CMFCore.interfaces import ISiteRoot

from Products.LinguaPlone.interfaces import ITranslatable
from AccessControl.SecurityManagement import getSecurityManager
from Products.LinguaPlone.browser.selector import TranslatableLanguageSelector


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
        # Exceptions: 1) If the object does not implement ITranslatable (= not
        # LP-aware) or
        # 2) if the object is set to be neutral
        # then return this object and don't look for a translation.
        context = aq_inner(self.context)
        translations = {}
        chain = aq_chain(context)
        first_pass = True
        _checkPermission = getSecurityManager().checkPermission
        for item in chain:
            if ISiteRoot.providedBy(item)
                or not ITranslatable.providedBy(item)
                or not item.Language():
                # We have a site root, which works as a fallback
                has_view_permission = bool(_checkPermission('View', item))
                for c in missing:
                    translations[c] = (item, first_pass, has_view_permission)
                break

            translatable = ITranslatable(item, None)
            if translatable is None:
                continue

            item_trans = item.getTranslations(review_state=False)
            for code, trans in item_trans.items():
                code = str(code)
                if code not in translations:
                    # make a link to a translation only if the user
                    # has view permission
                    has_view_permission = bool(_checkPermission('View', trans))
                    if (not INavigationRoot.providedBy(item)
                            and not has_view_permission):
                        continue
                    # If we don't yet have a translation for this language
                    # add it and mark it as found
                    translations[code] = (trans, first_pass,
                                          has_view_permission)
                    missing = missing - set((code, ))

            if len(missing) <= 0:
                # We have translations for all
                break
            if INavigationRoot.providedBy(item):
                # Don't break out of the navigation root jail
                has_view_permission = bool(_checkPermission('View', item))
                for c in missing:
                    translations[c] = (item, False, has_view_permission)
                break
            first_pass = False
        # return a dict of language code to tuple. the first tuple element is
        # the translated object, the second argument indicates wether the
        # translation is a direct translation of the context or something from
        # higher up the translation chain
        return translations
