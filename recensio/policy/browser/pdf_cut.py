from StringIO import StringIO

import pyPdf

from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent

from Products.statusmessages.interfaces import IStatusMessage
from Products.Five.browser import BrowserView

class PDFCutter(BrowserView):
    def __call__(self, sure = None):
        if sure:
            reader = pyPdf.PdfFileReader(self.context.pdf.blob.open())
            writer = pyPdf.PdfFileWriter()
            inputPages = [reader.getPage(i) for i in range(reader.getNumPages())]
            pages = inputPages[int(self.start_page):int(self.end_page)]
            for page in pages:
                writer.addPage(page)

            fakefile = StringIO()
            writer.write(fakefile)
            self.context.blob = fakefile
            IStatusMessage(self.request).addStatusMessage('PDF File has been cut', type='info')
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
