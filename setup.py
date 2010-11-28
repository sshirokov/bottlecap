#!/usr/bin/env python
import os, sys
import errno
import shutil
import subprocess
from setuptools import setup, find_packages
from optparse import OptionParser

BASEDIR = os.path.dirname(os.path.realpath(__file__))

setup(
    name='bottlecap',
    version='0.0.0',
    description = 'A tiny webserver',
    author      = 'slava@hackinggibsons.com',
    url         = 'https://github.com/sshirokov/bottlecap/',

    install_requires = ['bottle'],

    package_dir = {'': 'lib'},
    packages    = find_packages('lib'),

    entry_points = {
        'console_scripts': [
            'bottlecap = bottlecap.bin.bcap:main',
         ],
    },
)

