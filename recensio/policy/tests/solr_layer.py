"""This is copied from ploneintranet.search.solr.testing - we may want a separate egg"""
from glob import glob
from logging import getLogger
from pkg_resources import resource_filename
from plone.testing import Layer
from shutil import rmtree
from tempfile import mkdtemp
from zope.configuration import xmlconfig

import os
import requests
import subprocess
import sys
import time


logger = getLogger(__name__)

# This works well in a docker container
# /app/parts/test/../../bin => /app/bin
_BUILDOUT_DIR = os.path.abspath(os.path.join(os.getcwd(), os.pardir, os.pardir))

if not os.path.isdir(os.path.join(_BUILDOUT_DIR, "parts")):
    # This works well when using robot-server
    _BUILDOUT_DIR = os.getcwd()

SOLR_BUILDOUT_DIR = os.environ.get("SOLR_BUILDOUT_DIR", _BUILDOUT_DIR)
SOLR_TEST_PORT = int(os.environ.get("SOLR_TEST_PORT", 8984))


def load_solr_zcml():
    SOLR_ZCML = os.environ.get("SOLR_ZCML")
    if not SOLR_ZCML:
        SOLR_ZCML = resource_filename("ploneintranet.search.solr", "testing.zcml")
    xmlconfig.xmlconfig(open(SOLR_ZCML))


class SolrLayer(Layer):
    """A SOLR test layer that fires up and shuts down a SOLR instance.

    This layer can be used to unit test a Solr configuration without having to
    fire up Plone.
    """

    proc = None

    def __init__(
        self,
        bases=None,
        name=None,
        module=None,
        solr_host="localhost",
        solr_port=SOLR_TEST_PORT,
        solr_basepath="/solr",
    ):
        name = name if name is not None else type(self).__name__
        super().__init__(bases, name, module)
        self.solr_host = solr_host
        self.solr_port = solr_port
        self.solr_basepath = solr_basepath
        self.solr_url = f"http://{solr_host}:{solr_port}{solr_basepath}"
        self.solr_backup_dir = mkdtemp(prefix="ploneintranet-solr-tests-")
        self.solr_snapshot_name = "test"
        self.solr_snapshot_path = os.path.join(
            self.solr_backup_dir, f"snapshot.{self.solr_snapshot_name}"
        )

    def _solr_snapshot_exists(self):
        return os.path.isdir(self.solr_snapshot_path)

    def _solr_snapshot_remove(self):
        return rmtree(self.solr_snapshot_path)

    def _solr_snapshot(self):
        """Make a snapshot of the Solr data"""
        if self._solr_snapshot_exists():
            self._solr_snapshot_remove()
        requests.get(
            "{}/{}".format(self.solr_url, "core1/replication"),
            params={
                "command": "backup",
                "name": self.solr_snapshot_name,
                "location": self.solr_backup_dir,
            },
        )

    def _solr_verify_restore_not_in_progress(self):
        """Ping Solr until it says we do have a running restore"""
        while True:
            time.sleep(0.1)
            # Check the status of the restore, continue when ready
            status = requests.get(
                "{}/{}".format(self.solr_url, "core1/replication"),
                params={"command": "restorestatus"},
            )
            if "In Progress" not in status.text:
                return True

    def _solr_restore(self):
        """Make a restore of the Solr data snapshot"""
        requests.get(
            "{}/{}".format(self.solr_url, "core1/replication"),
            params={
                "command": "restore",
                "name": self.solr_snapshot_name,
                "location": self.solr_backup_dir,
            },
        )
        self._solr_verify_restore_not_in_progress()

    def _solr_start(self):
        list(
            map(
                rmtree,
                glob(
                    os.path.join(
                        SOLR_BUILDOUT_DIR,
                        "var",
                        "solr-test",
                        "solr",
                        "data",
                        "core1",
                        "restore*",
                    )
                ),
            )
        )
        with open(os.devnull, "w") as stdout:
            self.proc = subprocess.Popen(
                [
                    "/usr/bin/env",
                    "java",
                    "-jar",
                    "start.jar",
                    "--module=http",
                    "jetty.host=0.0.0.0",
                    f"jetty.port={self.solr_port}",
                ],
                cwd=os.path.join(SOLR_BUILDOUT_DIR, "parts", "solr-test"),
                stdout=stdout,
            )
        logger.info(f"SOLR instance (PID: {self.proc.pid})")

    def _solr_stop(self):
        self.proc.kill()

    def setUp(self):
        """Start Solr and poll until it is up and running."""
        self._solr_start()
        # Poll Solr until it is up and running
        solr_ping_url = f"{self.solr_url}/core1/admin/ping"
        n_attempts = 10
        i = 0
        while i < n_attempts:
            try:
                response = requests.get(solr_ping_url, timeout=1)
                if response.status_code == 200:
                    if '<str name="status">OK</str>' in response.text:
                        sys.stdout.write("[Solr Layer Connected] ")
                        sys.stdout.flush()
                        break
            except requests.ConnectionError:
                pass
            time.sleep(1)
            sys.stdout.write(".")
            sys.stdout.flush()
            i += 1

        if i == n_attempts:
            self._solr_stop()
            raise OSError("Solr Test Instance could not be started")

    def tearDown(self):
        """Stop Solr."""
        self._solr_stop()


SOLR_FIXTURE = SolrLayer()
