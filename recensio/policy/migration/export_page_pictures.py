from Acquisition import aq_base
from Products.Five.browser import BrowserView
from zope.component.hooks import getSite

import json


class ExportPagePictures(BrowserView):
    def __call__(self):
        """export_page_pictures view based on script from
        https://github.com/syslabcom/scrum/issues/883#issuecomment-1408728211
        """
        site = getSite()
        mapping = {}

        def findPagePictures(obj, obj_id):
            if getattr(aq_base(obj), 'pagePictures', None):
                mapping[obj.UID()] = []
                for field in obj.pagePictures:
                    with field.get(obj).blob.open():
                        mapping[obj.UID()].append(field.get(obj).blob._p_blob_committed)

        site.ZopeFindAndApply(site, search_sub=1, apply_func=findPagePictures)

        with open('pagePictures.json', 'w') as f:
            json.dump(mapping, f)
