from collective.exportimport.export_content import ExportContent
from collective.exportimport.interfaces import IBase64BlobsMarker
from collective.exportimport.interfaces import IPathBlobsMarker
from collective.exportimport.serializer import get_at_blob_path
from OFS.Image import Pdata
from plone.restapi.serializer.converters import json_compatible

import base64
import logging


logger = logging.getLogger(__name__)


class CustomExportContent(ExportContent):
    def global_dict_hook(self, item, obj):
        """collective.exportimport customizations."""

        # DOI export
        if "doi" in item:
            try:
                doi_active = obj.isDoiRegistrationActive()
            except AttributeError:
                doi_active = False
            if not doi_active and obj.getDoi() == obj.generateDoi():
                del item["doi"]

        # pagePictures export
        pagePictures = getattr(obj, "pagePictures", [])
        _pagePictures = []
        for pic in pagePictures:

            image = pic.get(obj)
            if not image:
                continue

            _item = {
                "filename": image.getFilename(),
                "content-type": image.getContentType(),
                "size": image.get_size(),
            }

            if hasattr(image, "height") and hasattr(image, "width"):
                _item["width"] = image.width
                _item["height"] = image.height

            if IBase64BlobsMarker.providedBy(self.request):
                data = image.data.data if isinstance(image.data, Pdata) else image.data
                _item["data"] = base64.b64encode(data)
                _item["encoding"] = "base64"

            elif IPathBlobsMarker.providedBy(self.request):
                blobfilepath = get_at_blob_path(image)
                if not blobfilepath:
                    logger.warning(
                        "Blob file path of %s does not exist",
                        obj.absolute_url(),
                    )
                    continue
                _item["blob_path"] = blobfilepath

            _pagePictures.append(json_compatible(_item))

        if _pagePictures:
            item["pagePictures"] = json_compatible(_pagePictures)

        return super(CustomExportContent, self).global_dict_hook(item, obj)
