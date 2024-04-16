from setuptools import find_packages
from setuptools import setup


version = "4.8.4"

setup(
    name="recensio.policy",
    version=version,
    description="Policy Product for the Recensio project",
    long_description=open("README.txt").read() + "\n" + open("CHANGES.txt").read(),
    classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python :: 2.7",
    ],
    keywords="plone zope recensio policy",
    author="Syslab.com GmbH",
    author_email="info@syslab.com",
    url="http://syslab.com/",
    license="GPL",
    packages=["vocabularies"] + find_packages(exclude=["ez_setup"]),
    namespace_packages=["recensio"],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "setuptools",
        "recensio.translations",
        "Products.CMFPlone",
        "rdflib",
        "rdflib-sparql",
        "sparql-client",
        "BeautifulSoup",
        "Products.ATVocabularyManager>=1.6",
        # Only here Plone 4 compatibility started
        "Products.CMFDiffTool>=2.0",
        # This fixed important issues related to Plone 4
        "Products.CMFPlacefulWorkflow",
        "Products.DataGridField",
        "Products.LinguaPlone",
        "collective.captcha>1.5",  # We have permission problems in 1.5
        "collective.indexing",
        "collective.portlet.tal",
        "guess-language",
        "lxml",
        "marcxml_parser",
        "paramiko",
        "plone.api",
        "plone.app.async",
        "plone.app.caching",
        "plone.app.discussion",
        "plone.app.intid",
        "plone.app.iterate",
        "plone.app.uuid",
        "pycountry",
        "pyoai",
        "python_memcached",
        "recensio.contenttypes",
        "recensio.imports",
        "recensio.theme",
        "requests",
        "setuptools",
        "slc.zopescript",
        "collective.logbook",
        # we need >=5.0 for getDataOrigin, see #14362, and the BlobError fix,
        # see #15018. We also need the cross-portal patch, see #13678
        "collective.solr>=5.0.4.dev0",
        "zope.app.pagetemplate",
        "zope.keyreference",
        "five.intid",  # Bugfix for plone.app.async
        "ftw.upgrade",
    ],
    extras_require={
        "test": ["plone.api", "plone.app.testing", "PILwoTk", "mock", "ipython"]
    },
    entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      [console_scripts]
      recensio-policy-reset = recensio.policy:reset
      createSite = recensio.policy:createSite
      metadata-export = recensio.policy.scripts.console_scripts:metadata_export
      chronicon-export = recensio.policy.scripts.console_scripts:chronicon_export
      newsletter = recensio.policy.scripts.console_scripts:newsletter
      sehepunkte-import = recensio.policy.scripts.console_scripts:sehepunkte_import
      register-all-dois = recensio.policy.scripts.console_scripts:register_all_dois
      """,
)
