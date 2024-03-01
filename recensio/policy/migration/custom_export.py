from collective.exportimport.export_content import ExportContent

class CustomExportContent(ExportContent):
    def global_dict_hook(self, item, obj):
        """ """
        if "doi" not in item:
            return super(CustomExportContent, self).global_dict_hook(item, obj)
        try:
            doi_active = obj.isDoiRegistrationActive()
        except AttributeError:
            doi_active = False
        if not doi_active and obj.getDoi() == obj.generateDoi():
            del item["doi"]
        return super(CustomExportContent, self).global_dict_hook(item, obj)
