#!/usr/bin/python
# -*- coding: utf-8 -*-

from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.browser.navtree import getNavigationRoot
from Products.Five.browser import BrowserView
import json


class SubjectList(BrowserView):

    def __call__(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        root = getNavigationRoot(self.context)
        facets = catalog({
            'path': root,
            'facet': 'true',
            'facet.field': 'Subject',
            'b_size': 0,
            'facet.limit': '-1',
            'facet.mincount': '1',
            }).facet_counts['facet_fields']['Subject'].items()
        facets.sort(key=lambda x: x[1])
        return json.dumps([x[0] for x in facets[:int(len(facets)
                          * 1)]])
