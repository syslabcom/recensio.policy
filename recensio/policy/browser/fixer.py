import urllib

from Products.Five.browser import BrowserView


class Fixer(BrowserView):
    def __call__(self):
        self.context.setCoverPicture(None)
        return "Deleted Cover image"
