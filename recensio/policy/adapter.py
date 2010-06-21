from plone.app.users.browser.personalpreferences import UserDataPanelAdapter

class RecensioUserDataPanelAdapter(UserDataPanelAdapter):
    """
    Use _getProperty so that all values are decoded from utf-8, all
    fields in the property sheet are stored as unicode.
    """

    def get_academic_title(self):
        return self._getProperty('academic_title')
    def set_academic_title(self, value):
        if value is not None:
            return self.context.setMemberProperties({'academic_title': value})
    academic_title = property(get_academic_title, set_academic_title)

    def get_preferred_language(self):
        return self._getProperty('preferred_language')
    def set_preferred_language(self, value):
        if value is not None:
            return self.context.setMemberProperties({'preferred_language': value})
    preferred_language = property(get_preferred_language, set_preferred_language)

