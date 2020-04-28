from StringIO import StringIO

import pyPdf
from Products.Five.browser import BrowserView
from Products.statusmessages.interfaces import IStatusMessage
from recensio.imports.pdf_cut import cutPDF
from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent


class PDFCutter(BrowserView):
    def __call__(self, sure=None):
        if sure:
            self.context.blob = cutPDF(
                self.context.pdf.blob.open(), self.start_page, self.end_page
            )

            IStatusMessage(self.request).addStatusMessage(
                "PDF File has been cut", type="info"
            )
            notify(ObjectModifiedEvent(self.context))
            return self.request.response.redirect(self.context.absolute_url())

        return self.index()

    @property
    def num_pages(self):
        reader = pyPdf.PdfFileReader(self.context.pdf.blob.open())
        return reader.getNumPages()

    @property
    def start_page(self):
        return self.context.pageStart

    @property
    def end_page(self):
        return self.context.pageEnd
