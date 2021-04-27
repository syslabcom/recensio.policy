from plone.app.users.browser.register import RegistrationForm


class RecensioRegistrationForm(RegistrationForm):
    """Adds project-specific tasks to registration"""

    def handle_join_success(self, data):
        """Set fullname from firstname and lastname"""
        if not getattr(data, "fullname", None):
            data["fullname"] = data["firstname"] + " " + data["lastname"]

        super(RecensioRegistrationForm, self).handle_join_success(data)

        return
