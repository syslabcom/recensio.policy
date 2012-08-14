from setuptools import setup, find_packages
import os

version = '2.5.4'

setup(name='recensio.policy',
      version=version,
      description="Policy Product for the Recensio project",
      long_description=open("README.txt").read() + "\n" +
                       open("CHANGES.txt").read(),
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='plone zope recensio policy',
      author='Syslab.com GmbH',
      author_email='info@syslab.com',
      url='http://syslab.com/',
      license='GPL',
      packages=['vocabularies'] + find_packages(exclude=['ez_setup']),
      namespace_packages=['recensio'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'rdflib',
          'sparql-client',
          'BeautifulSoup',
          'Products.ATVocabularyManager>=1.6', # Only here Plone 4 compatibility started
          'Products.CMFDiffTool>=2.0', # This fixed important issues related to Plone 4
          'Products.CMFPlacefulWorkflow',
          'Products.DataGridField',
          'Products.LinguaPlone',
          'collective.captcha>1.5', # We have permission problems in 1.5
          'collective.indexing',
          'collective.xdv',
          'collective.portlet.tal',
          'guess-language',
          'lxml',
          'plone.app.async',
          'plone.app.caching',
          'plone.app.discussion',
          'plone.app.iterate',
          'plone.app.uuid',
          'pyoai',
          'recensio.contenttypes',
          'recensio.imports',
          'recensio.theme',
          'recensio.translations',
          'setuptools',
          'collective.logbook',
          'collective.solr',
          'zope.keyreference',
      ],
      extras_require = {
        'test' : ['plone.app.testing', 'PILwoTk', 'mock', 'ipython']
      },
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      [console_scripts]
      recensio-policy-reset = recensio.policy:reset
      createSite = recensio.policy:createSite
      """,
      setup_requires=["PasteScript"],
      paster_plugins = ["ZopeSkel"],
      )
