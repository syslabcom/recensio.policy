from ftw.upgrade import UpgradeStep


class Scr1050(UpgradeStep):
    """scr-1050.
    """

    def __call__(self):
        self.install_upgrade_profile()
