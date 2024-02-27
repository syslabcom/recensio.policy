from collective.exportimport.export_content import ExportContent

class CustomExportContent(ExportContent):
    def dict_hook_document(self, item, obj):
        """ """
        if "doi" not in item:
            return item
        try:
            doi_active = obj.isDoiRegistrationActive()
        except AttributeError:
            doi_active = False
        if not doi_active and obj.getDoi() == obj.generateDoi():
            del item["doi"]
        return item
