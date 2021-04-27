from datetime import datetime
from os import path
from plone.uuid.interfaces import IUUID
from Products.Five.browser import BrowserView
from recensio.policy.constants import EXPORT_MAX_ITEMS
from recensio.policy.constants import EXPORT_OUTPUT_PATH
from recensio.policy.constants import EXPORTABLE_CONTENT_TYPES
from zope.app.pagetemplate import ViewPageTemplateFile

import logging


log = logging.getLogger(__name__)


class Book(object):
    def __init__(self, obj):
        issn = getattr(obj, "getIssn", lambda: None)
        self.isbn = getattr(obj, "getIsbn", issn)()
        self.subtitle = obj.title
        self.title = obj.getSubtitle()
        self.year = obj.getYearOfPublication()
        self.author_1 = {"first_name": "", "last_name": obj.getReviewAuthor()}
        self.author_2 = {"first_name": "", "last_name": ""}
        self.author_3 = {"first_name": "", "last_name": ""}

    @property
    def author(self):
        retval = None
        for i in range(1):  # We don't support multiple authors
            try:
                retval[i]["first_name"] = ""
                retval[i]["last_name"] = self.obj.getAuthors()
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
        for i in [range(1)]:  # No multiple authors support in our system
            yield {"last_name": self.obj.getAuthors(), "first_name": ""}

    @property
    def books(self):
        return [Book(self.obj) for x in [range(1)]]  # No multiple books
        # support in our system


class DigiToolRepresentation(BrowserView):
    """if this view is called, it iterates through the system and dumps every
    content type as xml to harddisk and marks it as exported with a little
    flag. If the flag is set, it is not exported again."""

    template = ViewPageTemplateFile("templates/digitool.pt")

    def __call__(self):
        return self.template(self)


class DigiToolExport(BrowserView):
    """if this view is called, it iterates through the system and dumps every
    content type as xml to harddisk and marks it as exported with a little
    flag. If the flag is set, it is not exported again."""

    def __call__(self):
        """run idempotent. Handle a number of records and return."""
        portal = self.context.portal_url.getPortalObject()

        now = datetime.now()
        count = 0
        for key, value in portal.ZopeFind(portal, search_sub=1):
            ob = value.aq_explicit
            if (
                hasattr(ob, "__digitool_exported__")
                or not hasattr(ob, "portal_type")
                or ob.portal_type not in EXPORTABLE_CONTENT_TYPES
            ):
                continue

            try:
                self.dump_xml(value)
            except KeyError, ke:
                print ke
                continue

            # setattr(value, '__digitool_exported__', True)
            count += 1
            if count > EXPORT_MAX_ITEMS:
                break

        delta = datetime.now() - now
        print "Exporting %s items takes %s secs" % (EXPORT_MAX_ITEMS, delta)
        return "ok %s" % delta

    def dump_xml(self, item):
        """create an xml representation of the object and dump it to disk"""

        data = item.unrestrictedTraverse("@@digitool-xml")
        filename = "%s/%s.xml" % (EXPORT_OUTPUT_PATH, IUUID(item))
        if path.exists(filename):
            print "File exists, overwriting"
            # raise KeyError, "File exists, but must not"

        fh = open(filename, "w")
        fh.write(data())
        fh.close()

    @property
    def reviews(self):
        return [Review(x) for x in self.context.queryCatalog()]
