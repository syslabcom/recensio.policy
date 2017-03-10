from Products.Five.browser import BrowserView
from Products.statusmessages.interfaces import IStatusMessage
from datetime import date
from paramiko import SFTPClient
from paramiko import Transport
from paramiko.ssh_exception import SSHException
from plone import api
from plone.registry.interfaces import IRegistry
from recensio.contenttypes.interfaces.review import IReview
from recensio.policy.export import LZAExporter
from recensio.policy.export import register_doi
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
        if self.request.get('force', False):
            del annotations[EXPORT_TIMESTAMP_KEY]
        timestamp = annotations.get(EXPORT_TIMESTAMP_KEY, 0)
        if time() - timestamp < 2 * 60 * 60:  # 2 hours
            log.info('export already running, abort')
            return 'An export is already running, aborting'

        annotations[EXPORT_TIMESTAMP_KEY] = time()
        transaction.commit()

        try:
            exporters = [(name, factory()) for name, factory in
                        getFactoriesFor(IRecensioExporter)]
            exporters_to_run = [(name, e) for name, e in exporters
                                if e.needs_to_run()]
        except Exception as e:
            log.exception(e)
            del annotations[EXPORT_TIMESTAMP_KEY]
            msg = 'Error, aborting export: ' + str(e)
            log.error(msg)
            return msg

        if not exporters_to_run:
            del annotations[EXPORT_TIMESTAMP_KEY]
            log.info('export finished, nothing to do')
            return 'Nothing to do, no exporter requested an export run.'

        for issue_or_volume in self.issues_and_volumes():
            for review in self.reviews(issue_or_volume):
                for name, exporter in exporters_to_run:
                    try:
                        exporter.add_review(review)
                    except Exception as e:
                        log.error('Error in {0} - {1}: {2}'.format(
                            review.getId(), e.__class__.__name__, e))
            # Free memory after every issue and volume
            transaction.commit()
        statuses = []
        for name, exporter in exporters_to_run:
            try:
                status = exporter.export()
                statuses.append((name, status))
            except Exception as e:
                log.error('Error in {0} - {1}: {2}'.format(
                    name, e.__class__.__name__, e))

        del annotations[EXPORT_TIMESTAMP_KEY]
        transaction.commit()
        log.info('export finished')

        return '<br />\n'.join(
            [name + ': ' + str(status) for name, status in statuses])

    def issues_and_volumes(self):
        pc = api.portal.get_tool('portal_catalog')
        parent_path = dict(query='/'.join(self.context.getPhysicalPath()))
        results = pc(review_state="published",
                     portal_type=("Issue", "Volume"),
                     path=parent_path)
        for item in results:
            try:
                yield item.getObject()
            except AttributeError:
                log.warn('Could not getObject: ' + item.getPath())
                continue

    def reviews(self, issue):
        pc = api.portal.get_tool('portal_catalog')
        parent_path = dict(query='/'.join(issue.getPhysicalPath()),
                           depth=1)
        results = pc(review_state="published",
                     portal_type=("Review Monograph", "Review Journal"),
                     path=parent_path)
        for item in results:
            try:
                yield item.getObject()
            except AttributeError:
                log.warn('Could not getObject: ' + item.getPath())
                continue


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


class DaraUpdate(BrowserView):
    """Send metadata to da|ra, in effect registering the object's DOI or
    updating its metadata if already registered."""

    def __call__(self):
        if self.request.get('REQUEST_METHOD') == 'POST':
            status, message = register_doi(self.context)
            IStatusMessage(self.request).addStatusMessage(
                message, type=status)
        self.request.response.redirect(self.context.absolute_url())


class ResetLZAExportFlag(BrowserView):

    def _reset_flag(self, context):
        paths = []
        if IReview.providedBy(context):
            self.exporter._set_exported(context, value=False)
            paths.append('/'.join(context.getPhysicalPath()))
        for child in getattr(context, 'objectValues', lambda: [])():
            paths += self._reset_flag(child)
        return paths

    def __call__(self):
        self.exporter = LZAExporter()
        paths = self._reset_flag(self.context)
        return (u"Reset LZA export flag for the following objects:\n\n" +
                u'\n'.join(paths))
