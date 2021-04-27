# taken from wildcard.pdfpal, thanks a lot!

from DateTime import DateTime
from os import fstat
from Products.Archetypes.utils import contentDispositionHeader
from Products.ATContentTypes.interface.file import IFileContent
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import base_hasattr
from Products.Five import BrowserView
from webdav.common import rfc1123_date
from zope.component import getUtility
from zope.formlib import form


def time_since(dt):
    now = DateTime("UTC")
    diff = now - dt

    secs = int(diff * 24 * 60 * 60)
    minutes = secs / 60
    hours = minutes / 60
    days = hours / 24

    if days:
        return "%i day%s" % (days, days > 1 and "s" or "")
    elif hours:
        return "%i hour%s" % (hours, hours > 1 and "s" or "")
    elif minutes:
        return "%i minute%s" % (minutes, minutes > 1 and "s" or "")
    else:
        return "%i second%s" % (secs, secs > 1 and "s" or "")


try:
    from plone.app.async.interfaces import IAsyncService

    paa_installed = True
except:
    paa_installed = False


class AsyncMonitor(BrowserView):
    """ """

    def get_job_data(self, job):
        lastused = DateTime(job._p_mtime)
        if len(job.args) > 3:
            user = job.args[3]
        else:
            user = ""
        if len(job.args) > 4:
            intro = job.args[4]
        else:
            intro = {}
        if isinstance(job.args[0], list):
            object_path = "/".join(job.args[0])
        else:
            object_path = str(job.args[0])

        if job.status != "pending-status":
            timerunning = time_since(lastused)
        else:
            timerunning = "-"
        return {
            "status": job.status,
            "user": user,
            "object_path": object_path,
            "description": (
                getattr(intro, "__doc__", "") or getattr(intro, "__name__", "")
            ).strip(),
            "lastused": lastused.toZone("UTC").pCommon(),
            "timerunning": timerunning,
        }

    @property
    def jobs(self):
        results = []

        if paa_installed:
            async = getUtility(IAsyncService)
            queue = async.getQueues()[""]

            for quota in queue.quotas.values():
                for job in quota._data:
                    results.append(self.get_job_data(job))

            jobs = [job for job in queue]
            for job in jobs:
                results.append(self.get_job_data(job))

        return results
