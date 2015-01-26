from Products.Five.browser import BrowserView
from datetime import date
from paramiko import SFTPClient
from paramiko import Transport
from paramiko.ssh_exception import SSHException
from plone.registry.interfaces import IRegistry
from recensio.policy.interfaces import IRecensioExporter
from recensio.policy.interfaces import IRecensioSettings
from time import time
from zope.annotation.interfaces import IAnnotations
from zope.component import getFactoriesFor
from zope.component import getUtility
from zope.component.interfaces import IFactory
import logging
import transaction

log = logging.getLogger(__name__)

EXPORT_TIMESTAMP_KEY = 'recensio.policy.metadata_export_timestamp'


class MetadataExport(BrowserView):

    def __call__(self):
        log.info('Starting export')
        annotations = IAnnotations(self.context)
        timestamp = annotations.get(EXPORT_TIMESTAMP_KEY, 0)
        if time() - timestamp < 2 * 60 * 60:  # 2 hours
            log.info('export already running, abort')
            return 'An export is already running, aborting'

        annotations[EXPORT_TIMESTAMP_KEY] = time()
        transaction.commit()

        exporters = [(name, factory()) for name, factory in
                     getFactoriesFor(IRecensioExporter)]
        exporters_to_run = [(name, e) for name, e in exporters
                            if e.needs_to_run()]
        if not exporters_to_run:
            del annotations[EXPORT_TIMESTAMP_KEY]
            log.info('export finished, nothing to do')
            return 'Nothing to do, no exporter requested an export run.'

        for issue in self.issues():
            for review in self.reviews(issue):
                for name, exporter in exporters_to_run:
                    try:
                        exporter.add_review(review)
                    except Exception as e:
                        log.error('Error in {0} - {1}: {2}'.format(
                            review.getId(), e.__class__.__name__, e))
        statuses = []
        for name, exporter in exporters_to_run:
            try:
                status = exporter.export()
                statuses.append((name, status))
            except Exception as e:
                log.error('Error in {0} - {1}: {2}'.format(
                    name, e.__class__.__name__, e))

        del annotations[EXPORT_TIMESTAMP_KEY]
        log.info('export finished')

        return '<br />\n'.join(
            [name + ': ' + str(status) for name, status in statuses])

    def issues(self):
        pc = self.context.portal_catalog
        parent_path = dict(query='/'.join(self.context.getPhysicalPath()))
        results = pc(review_state="published",
                     portal_type=("Issue"),
                     path=parent_path)
        for item in results:
            yield item.getObject()

    def reviews(self, issue):
        pc = self.context.portal_catalog
        parent_path = dict(query='/'.join(issue.getPhysicalPath()),
                           depth=3)
        results = pc(review_state="published",
                     portal_type=("Review Monograph", "Review Journal"),
                     path=parent_path)
        for item in results:
            yield item.getObject()


class ChroniconExport(BrowserView):

    @property
    def filename(self):
        return "recensio_%s_all.zip" % (
            date.today().strftime("%d%m%y"),
        )

    def __call__(self):
        registry = getUtility(IRegistry)
        recensio_settings = registry.forInterface(IRecensioSettings)
        host = recensio_settings.xml_export_server
        username = recensio_settings.xml_export_username
        password = recensio_settings.xml_export_password
        if not host:
            return 'no host configured'
        log.info("Starting XML export to sftp")

        exporter = getUtility(IFactory, name='chronicon_exporter')()
        export_xml = exporter.get_export_obj(self.context)
        if export_xml is None:
            msg = "Could not get export file object: {0}".format(
                exporter.export_filename)
            log.error(msg)
            return msg

        zipstream = export_xml.getFile()
        try:
            transport = Transport((host, 22))
            transport.connect(username=username, password=password)
            sftp = SFTPClient.from_transport(transport)
            attribs = sftp.putfo(zipstream.getBlob().open(), self.filename)
        except (IOError, SSHException) as ioe:
            msg = "Export failed, {0}: {1}".format(ioe.__class__.__name__, ioe)
            log.error(msg)
            return msg
        if attribs.st_size == zipstream.get_size():
            msg = "Export successful"
            log.info(msg)
            return msg
        else:
            msg = "Export failed, {0}/{1} bytes transferred".format(
                attribs.st_size, zipstream.get_size())
            log.error(msg)
            return msg
