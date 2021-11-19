# -*- coding: utf-8 -*-
from ftw.upgrade import UpgradeStep
from plone import api
from plone.app.discussion.conversation import ANNOTATION_KEY
from zope.annotation.interfaces import IAnnotations
import logging

logger = logging.getLogger(__name__)


class DeleteAllComments(UpgradeStep):
    """Delete all comments."""

    def __call__(self):
        self.install_upgrade_profile()
        portal_catalog = api.portal.get_tool("portal_catalog")
        query = dict(
            total_comments={"query": 1, "range": "min"},
            b_size=10000,
            facet_field="portal_type",
        )
        commented_items = portal_catalog(query)
        if len(commented_items) > 10000:
            query["b_size"] = len(commented_items)
            commented_items = portal_catalog(query)
        logger.info("Objects with comments: {}".format(len(commented_items)))
        logger.info(
            {
                ptype: num
                for ptype, num in commented_items.facet_counts["facet_fields"][
                    "portal_type"
                ].items()
                if num > 0
            }
        )

        count = 0
        for brain in commented_items:
            try:
                obj = brain.getObject()
            except Exception as e:
                logger.exception(e)
                continue
            annotations = IAnnotations(obj)
            if ANNOTATION_KEY in annotations:
                del annotations[ANNOTATION_KEY]
                count += 1
            # if there is no annotation but we still got the object from the catalog,
            # maybe it just needs reindexing?
            obj.reindexObject()
        logger.info("Deleted comments from {} objects".format(count))
