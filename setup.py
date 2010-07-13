from setuptools import setup, find_packages
import os

version = '1.0'

setup(name='recensio.policy',
      version=version,
      description="Policy Product for the Recensio project",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='plone zope recensio policy',
      author='Syslab.com GmbH',
      author_email='info@syslab.com',
      url='http://syslab.com/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['recensio'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'Products.ATVocabularyManager',
          'Products.CMFPlacefulWorkflow',
          'Products.DataGridField',
          'Products.LinguaPlone',
          'collective.captcha',
          'collective.indexing',
          'collective.xdv',
          'plone.app.discussion',
          'plone.app.iterate',
          'plone.contentratings',
          'recensio.contenttypes',
          'recensio.imports',
          'recensio.theme',
          'setuptools',
          'wc.pageturner',
          'collective.solr',
      ],
      extras_require = {
        'test' : ['plone.app.testing']
      },
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      setup_requires=["PasteScript"],
      paster_plugins = ["ZopeSkel"],
      )
