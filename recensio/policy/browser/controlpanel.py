from Products.Five.browser import BrowserView

from zope.component import queryUtility
from plone.registry.interfaces import IRegistry

from plone.app.registry.browser import controlpanel

from recensio.policy.interfaces import IRecensioSettings
from recensio.policy import recensioMessageFactory as _


class RecensioSettingsEditForm(controlpanel.RegistryEditForm):

    schema = IRecensioSettings
    label = _(u"label_recensio_settings", default=u"Recensio settings")
    description = _(u"description_recensio_setings", default=u"Below are some "
        "options for configuring the recensio portal.")
        
        
class RecensioSettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    form = RecensioSettingsEditForm    