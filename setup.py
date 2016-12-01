#!/usr/bin/env python
'''Making it pip-installable'''
import os
import codecs
import setuptools


PACKAGENAME = 'sqre-github-snapshot'
DESCRIPTION = 'LSST Data Management SQuaRE Github Organization Snapshotter'
AUTHOR = 'Adam Thornton'
AUTHOR_EMAIL = 'athornton@lsst.org'
URL = 'https://github.com/lsst-sqre/sqre-github-snapshots/'
VERSION = '0.1.0'
LICENSE = 'MIT'


def read(filename):
    '''Convenience function to do, basically, an include'''
    full_filename = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        filename)
    return codecs.open(full_filename, 'r', 'utf-8').read()

LONG_DESCRIPTION = read('README.md')

setuptools.setup(
    name=PACKAGENAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    url=URL,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license=LICENSE,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 2.7',
        'License :: OSI Approved :: MIT License',
    ],
    keywords='lsst',
    packages=setuptools.find_packages(exclude=['docs', 'tests*']),
    install_requires=[
        'github3.py==1.0.0a4',
        'requests==2.8.1',
        'progressbar2==3.11.0',
        'awscli==1.11.21',
        'sqre-codekit==1.0.1',
        'MapGitConfig==1.1',
        'uritemplate.py==2.0.0'  # Ugh.  Not pulled in by codekit.
    ],
    entry_points={
        'console_scripts': [
            'github-snapshot = github_snapshot.github_snapshot:main',
            'snapshot-purger = github_snapshot.snapshot_purger:main'
        ]
    }
)
