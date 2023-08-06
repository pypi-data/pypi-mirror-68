#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('docs\HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click>=6.0', ]

setup_requirements = [ ]

test_requirements = [ ]

setup(
    author="Morgan Allison",
    author_email='morgan.allison@keysight.com',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="socketscpi provides a robust SCPI interface to electronic test and measurement equipment via raw socket protocol, removing the requirement for VISA and improving data transfer speed over VXI-11.",
    entry_points={
        'console_scripts': [
            'socketscpi=socketscpi.cli:main',
        ],
    },
    packages=find_packages(exclude=['docs', 'tests']),
    install_requires=['numpy'],
    license="GNU General Public License v3",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='socketscpi',
    name='socketscpi',
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/morgan-at-keysight/socketscpi',
    version='2020.05.0',
    zip_safe=False,
)
