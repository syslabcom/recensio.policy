# taken from wildcard.pdfpal, thanks a lot!

from Products.Five import BrowserView
from zope.component import getUtility
from Products.CMFPlone.utils import base_hasattr
from Products.Archetypes.utils import contentDispositionHeader
from os import fstat
from webdav.common import rfc1123_date
from zope.formlib import form
from Products.CMFCore.utils import getToolByName
from DateTime import DateTime
from Products.ATContentTypes.interface.file import IFileContent

def time_since(dt):
    now = DateTime('UTC')
    diff = now - dt
    
    secs = int(diff*24*60*60)
    minutes = secs/60
    hours = minutes/60
    days = hours/24
    
    if days:
        return '%i day%s' % (days, days > 1 and 's' or '')
    elif hours:
        return '%i hour%s' % (hours, hours > 1 and 's' or '')
    elif minutes:
        return '%i minute%s' % (minutes, minutes > 1 and 's' or '')
    else:
        return '%i second%s' % (secs, secs > 1 and 's' or '')


try:
    from plone.app.async.interfaces import IAsyncService
    paa_installed = True
except:
    paa_installed = False

class AsyncMonitor(BrowserView):
    """
    
    """
    
    def get_job_data(self, job):
        lastused = DateTime(job._p_mtime)
        if job.status != 'pending-status':
            timerunning = time_since(lastused)
        else:
            timerunning = '-'
        return {
            'status' : job.status,
            'user' : job.args[3],
            'object_path' : '/'.join(job.args[0]),
            'description' : (getattr(job.args[4], '__doc__') or job.args[4].__name__).strip(),
            'lastused' : lastused.toZone('UTC').pCommon(),
            'timerunning' : timerunning
        }
    
    @property
    def jobs(self):
        results = []
        
        if paa_installed:
            async = getUtility(IAsyncService)
            queue = async.getQueues()['']
        
            for quota in queue.quotas.values():
                for job in quota._data:
                    results.append(self.get_job_data(job))        
        
            jobs = [job for job in queue]
            for job in jobs:
                results.append(self.get_job_data(job))
            
        return results
