import logging

import transaction
from plone.registry.interfaces import IRegistry
from Products.CMFCore.utils import getToolByName
from zope import component

log = logging.getLogger("recensio.profile/setuphandlers.py")
