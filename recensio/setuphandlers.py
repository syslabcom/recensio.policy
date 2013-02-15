import logging
import transaction

from zope import component

from Products.CMFCore.utils import getToolByName
from plone.registry.interfaces import IRegistry


log = logging.getLogger('recensio.profile/setuphandlers.py')

