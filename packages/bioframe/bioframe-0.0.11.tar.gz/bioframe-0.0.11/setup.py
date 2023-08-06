#!/usr/bin/env python
# -*- coding: utf-8 -*-
import io
import os
import re

from setuptools import setup, find_packages


PKG_NAME = 'bioframe'
README_PATH = 'README.md'


classifiers = """\
    Development Status :: 3 - Alpha
    Operating System :: OS Independent
    Programming Language :: Python
    Programming Language :: Python :: 2
    Programming Language :: Python :: 2.7
    Programming Language :: Python :: 3
    Programming Language :: Python :: 3.3
    Programming Language :: Python :: 3.4
    Programming Language :: Python :: 3.5
    Programming Language :: Python :: 3.6
    Programming Language :: Python :: 3.7
"""


def _read(*parts, **kwargs):
    filepath = os.path.join(os.path.dirname(__file__), *parts)
    encoding = kwargs.pop('encoding', 'utf-8')
    with io.open(filepath, encoding=encoding) as fh:
        text = fh.read()
    return text


def get_version():
    version = re.search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
        _read('{}/_version.py'.format(PKG_NAME)),
        re.MULTILINE).group(1)
    return version


# def get_long_description():
#     descr = _read(README_PATH)
#     try:
#         import pypandoc
#         descr = pypandoc.convert_text(descr, to='rst', format='md')
#     except (IOError, ImportError):
#         pass
#     return descr
def get_long_description():
    return _read(README_PATH)


install_requires = [
    'six',
    'numpy>=1.9',
    'pandas>=0.17',
    'pysam',
    'pyfaidx',
    'pypairix',
    'requests',
]


# tests_require = [
#     'nose',
#     'mock'
# ]


# extras_require = {
#     'docs': [
#         'Sphinx>=1.1',
#         'numpydoc>=0.5'
#     ]
# }


setup(
    name=PKG_NAME,
    author='Nezar Abdennur',
    author_email='nezar@mit.edu',
    version=get_version(),
    license='MIT',
    description='Pandas utilities for tab-delimited and other genomic files',
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    url='https://github.com/mirnylab/bioframe',
    keywords=['pandas', 'dataframe', 'genomics', 'epigenomics', 'bioinformatics'],
    packages=find_packages(),
    zip_safe=False,
    classifiers=[s.strip() for s in classifiers.split('\n') if s],
    install_requires=install_requires,
    # tests_require=tests_require,
    # extras_require=extras_require,
    # entry_points={
    # }
)
