#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function

import io
import re
from glob import glob
from os.path import basename
from os.path import dirname
from os.path import join
from os.path import splitext

from setuptools import find_packages
from setuptools import setup


def read(*names, **kwargs):
    with io.open(
        join(dirname(__file__), *names),
        encoding=kwargs.get('encoding', 'utf8')
    ) as fh:
        return fh.read()


setup(
    name='at-bat-scraper',
    version='0.1',
    license='MIT License',
    description='Package to scrape at-bat level data from the web for both hitters and pitchers.',
    long_description='''
        Package that utilizes selenium to scrape at-bat level player data on
        both mlb.com and baseballsavant.mlb.com; returning them as csv files
        or as dictionaries.
    ''',
    author='Benjamin Hammack',
    author_email='bjhammack@protonmail.com',
    url='https://github.com/bjhammack/at-bat-scraper',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Utilities',
    ],
    project_urls={
        'Changelog': 'https://github.com/bjhammack/at-bat-scraper/blob/master/CHANGELOG.rst',
        'Issue Tracker': 'https://github.com/bjhammack/at-bat-scraper/issues',
    },
    keywords=[
        # eg: 'keyword1', 'keyword2', 'keyword3',
    ],
    python_requires='>=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*',
    install_requires=[
        '-e git+git@github.com:bjhammack/at-bat-scraper.git@c5cf9ad56e7563b1ee486296a719816ee7e4cf61#egg=at_bat_scraper',
        'certifi>=2021.5.30',
        'charset-normalizer>=2.0.6',
        'colorama>=0.4.4',
        'configparser>=5.0.2',
        'crayons>=0.4.0',
        'idna>=3.2',
        'numpy>=1.21.2',
        'pandas>=1.3.3',
        'python-dateutil>=2.8.2',
        'pytz>=2021.1',
        'requests>=2.26.0',
        'selenium>=3.141.0',
        'six>=1.16.0',
        'urllib3>=1.26.7',
        'webdriver-manager>=3.4.2',
    ],
    extras_require={
        # eg:
        #   'rst': ['docutils>=0.11'],
        #   ':python_version=="2.6"': ['argparse'],
    },
    setup_requires=[
        
    ],
    entry_points={
        'console_scripts': [
            'player = scrape_player.player:main',
        ]
    },
)