from plone.registry.interfaces import IRegistry
from Products.CMFCore.utils import getToolByName
from zope import component

import logging
import transaction


log = logging.getLogger("recensio.profile/setuphandlers.py")
