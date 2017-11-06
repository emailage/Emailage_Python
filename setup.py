#!/usr/bin/env python

"""Setup script for Emailage."""

import setuptools

from emailage import __project__, __version__

try:
    README = open("README.rst").read()
    CHANGES = open("CHANGES.rst").read()
except IOError:
    DESCRIPTION = "The Emailage (TM) API is organized around REST (Representational State Transfer). The API was built to help companies integrate with our highly efficient fraud risk and scoring system. By calling our API endpoints and simply passing us an email and/or IP Address, companies will be provided with real-time risk scoring assessments based around machine learning and proprietary algorithms that evolve with new fraud trends."
else:
    DESCRIPTION = README + '\n' + CHANGES

setuptools.setup(
    name=__project__,
    version=__version__,

    description="Official Emailage API client written in Python",
    url='https://www.emailage.com/',
    author='Emailage Dev Team',
    author_email='dev@emailage.com',

    packages=setuptools.find_packages(),

    entry_points={'console_scripts': []},

    long_description=(DESCRIPTION),
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
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
