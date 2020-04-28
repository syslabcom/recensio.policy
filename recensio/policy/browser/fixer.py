from Products.Five.browser import BrowserView
import urllib


class Fixer(BrowserView):
    def __call__(self):
        self.context.setCoverPicture(None)
        return "Deleted Cover image"
