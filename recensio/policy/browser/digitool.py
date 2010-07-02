from Products.Five.browser import BrowserView
from zope.app.pagetemplate import ViewPageTemplateFile

class Book(object):
    def __init__(self, obj):
        self.isbn = getattr(obj, 'getIsbn', getattr(obj, 'getIssn', lambda: None))()
        self.subtitle = obj.title
        self.title = obj.getSubtitle()
        self.year = obj.getYearOfPublication()
        self.author_1 = {'first_name' : '', 'last_name' : obj.getReviewAuthor()}
        self.author_2 = {'first_name' : '', 'last_name' : ''}
        self.author_3 = {'first_name' : '', 'last_name' : ''}

    @property
    def author(self):
        for i in range(1): # We don't support multiple authors
            try:
                retval[i]['first_name'] = ''
                retval[i]['last_name'] = self.obj.getAuthors()
            except IndexError:
                pass
        return retval

class Review(object):
    def __init__(self, catalog_entry):
        self.obj = catalog_entry.getObject()
        self.id = catalog_entry.getPath()
        self.filename = catalog_entry.getURL()

    @property
    def reviewers(self):
        for i in [range(1)]: # No multiple authors support in our system
            yield {'last_name' : self.obj.getAuthors(),
                   'first_name' : ''}

    @property
    def books(self):
        return [Book(self.obj) for x in [range(1)]] # No multiple books support
                                                   # in our system

class DigiToolRepresentation(BrowserView):
    template = ViewPageTemplateFile('templates/digitool.pt')

    def __call__(self):
        self.number = 'fake'
        self.volume = 'fake'
        self.year = 'fake'
        return self.template(self)

    @property
    def reviews(self):
        return [Review(x) for x in self.context.queryCatalog()]
