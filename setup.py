#!/usr/bin/env python

# Standard library modules.
import os
import sys
import logging

# Third party modules.
from setuptools import setup, find_packages

# Local modules.
import versioneer

# Globals and constants variables.
logger = logging.getLogger(__name__)
BASEDIR = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(BASEDIR, 'README.rst'), 'r') as fp:
    LONG_DESCRIPTION = fp.read()

PACKAGES = find_packages(include=['pipeline_async'])

with open(os.path.join(BASEDIR, 'requirements.txt'), 'r') as fp:
    INSTALL_REQUIRES = fp.read().splitlines()

EXTRAS_REQUIRE = {}
with open(os.path.join(BASEDIR, 'requirements_dev.txt'), 'r') as fp:
    EXTRAS_REQUIRE['dev'] = fp.read().splitlines()

CMDCLASS = versioneer.get_cmdclass()

ENTRY_POINTS = {}

setup(
    name='pipeline-async',
    version=versioneer.get_version(),
    url='https://github.com/ppinard/pipeline-async',
    author="Philippe Pinard",
    author_email='philippe.pinard@gmail.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],
    description="Execute pipeline asynchronously",
    long_description=LONG_DESCRIPTION,
    license="Apache Software License 2.0",

    packages=PACKAGES,
    include_package_data=True,

    install_requires=INSTALL_REQUIRES,
    extras_require=EXTRAS_REQUIRE,

    cmdclass=CMDCLASS,

    entry_points=ENTRY_POINTS,
)

