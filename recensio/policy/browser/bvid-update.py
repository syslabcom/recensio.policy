from plone import api
from Products.Five.browser import BrowserView

import csv


class BVIDUpdate(BrowserView):
    """Read a CSV of UID, ISBN and BVID and update the BVID field of the
    corresponding review object.
    """

    def __call__(self):
        self.update_successful = None
        if self.request.get("REQUEST_METHOD") == "POST":
            self.do_update()
        return self.index()

    def do_update(self):
        self.errors = []
        self.updated = []
        self.update_successful = True
        csv_file = self.request.get("csv_file")
        csvreader = csv.reader(csv_file)
        for uid, _, bvid in csvreader:
            obj = api.content.get(UID=uid)
            if obj is None:
                self.update_successful = False
                self.errors.append("Konnte Objekt nicht finden: " + uid)
                continue
            if obj.getBv() != bvid:
                obj.setBv(bvid)
                self.updated.append(uid)
