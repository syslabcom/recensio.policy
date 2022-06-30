from ftw.upgrade import UpgradeStep


class UninstallRecensioArtium(UpgradeStep):
    """Uninstall recensio.artium.
    """

    def __call__(self):
        if self.is_product_installed("recensio.artium:default"):
            self.uninstall_product("recensio.artium:default")
