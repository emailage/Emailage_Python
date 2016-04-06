#!/usr/bin/env python

"""Setup script for Emailage."""

import setuptools

from emailage import __project__, __version__

try:
    README = open("README.rst").read()
    CHANGES = open("CHANGES.rst").read()
except IOError:
    DESCRIPTION = "<placeholder>"
else:
    DESCRIPTION = README + '\n' + CHANGES

setuptools.setup(
    name=__project__,
    version=__version__,

    description="Emailage API client written in Python",
    url='https://emailage.com/',
    author='Sergey Baev',
    author_email='tinbka@gmail.com',

    packages=setuptools.find_packages(),

    entry_points={'console_scripts': []},

    long_description=(DESCRIPTION),
    license='MIT',
    classifiers=[
        # TODO: update this list to match your application: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 5 - Production/Stable',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    install_requires=open("requirements.txt").readlines(),
)
