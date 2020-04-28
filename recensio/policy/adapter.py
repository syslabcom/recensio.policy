from plone.app.users.browser.personalpreferences import UserDataPanelAdapter
from Products.CMFPlone.browser.syndication.adapters import (
    SearchFeed as SearchFeedBase)
from Products.CMFPlone.interfaces.syndication import ISearchFeed
from zope.interface import implements


class RecensioUserDataPanelAdapter(UserDataPanelAdapter):
    """
    Use _getProperty so that all values are decoded from utf-8, all
    fields in the property sheet are stored as unicode.
    """

    def get_academic_title(self):
        return self._getProperty("academic_title")

    def set_academic_title(self, value):
        if value is not None:
            return self.context.setMemberProperties({"academic_title": value})

    academic_title = property(get_academic_title, set_academic_title)

    def get_preferred_language(self):
        return self._getProperty("preferred_language")

    def set_preferred_language(self, value):
        if value is not None:
            return self.context.setMemberProperties({"preferred_language": value})

    preferred_language = property(get_preferred_language, set_preferred_language)

    def get_firstname(self):
        return self._getProperty("firstname")

    def set_firstname(self, value):
        if value is not None:
            return self.context.setMemberProperties({"firstname": value})

    firstname = property(get_firstname, set_firstname)

    def get_lastname(self):
        return self._getProperty("lastname")

    def set_lastname(self, value):
        if value is not None:
            return self.context.setMemberProperties({"lastname": value})

    lastname = property(get_lastname, set_lastname)

    def get_declaration_of_identity(self):
        return self._getProperty("declaration_of_identity")

    def set_declaration_of_identity(self, value):
        if value is not None:
            return self.context.setMemberProperties({"declaration_of_identity": value})

    declaration_of_identity = property(
        get_declaration_of_identity, set_declaration_of_identity
    )

    captcha = None

    def absolute_url(self):
        return "recensio"


class SearchFeed(SearchFeedBase):
    implements(ISearchFeed)

    def _brains(self):
        max_items = self.limit
        request = self.context.REQUEST
        start = int(request.get("b_start", 0))
        end = int(request.get("b_end", start + max_items))
        request.set("sort_order", "reverse")
        request.set("sort_on", request.get("sort_on", "effective"))
        return self.context.queryCatalog(
            show_all=1,
            use_types_blacklist=True,
            use_navigation_root=True,
            b_start=start,
            b_size=max_items,
        )[start:end]
