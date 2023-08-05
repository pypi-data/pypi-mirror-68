#!/usr/bin/env python3
from setuptools import setup


from djangocms_helpers import __version__


setup(
    name='djangocms-algolia',
    version=__version__,
    author='Victor Yunenko',
    author_email='victor@what.digital',
    url='https://gitlab.com/victor-yunenko/djangocms-algolia',
    packages=[
        'djangocms_algolia',
    ],
    include_package_data=True,
    install_requires=[
        'django >= 2.2, < 3',
        'django-cms >= 3.7.2, < 4',
        'algoliasearch-django',
        'aldryn-search',
    ],
)
