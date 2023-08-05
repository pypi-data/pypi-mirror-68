#!/usr/bin/env python

from setuptools import setup, find_packages
from os import path


def read(*paths):
    filename = path.join(path.abspath(path.dirname(__file__)), *paths)
    with open(filename) as f:
        return f.read()


setup(
    name='tap-typo',
    version='0.2.0',
    description=(
        'Typo is the intelligent data quality barrier for '
        'enterprise information systems. The Typo tap '
        'retrieves results and data from the Typo platform.'),
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    author='Typo',
    keywords='typo.ai data quality singer tap',
    url='https://www.typo.ai/',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Topic :: Database :: Database Engines/Servers',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ],
    py_modules=['tap_typo'],
    packages=find_packages(),
    package_data={
        'schemas': ['tap_typo/schemas/*.json']
    },
    include_package_data=True,
    install_requires=[
        'singer-python>=5.0.12',
        'requests>=2.21.0',
        'jsonschema>=2.6.0,<3.0a',
        'backoff==1.8.0',
        'rfc3339==6.2'
    ],
    entry_points={
        'console_scripts': [
            'tap-typo=tap_typo:main',
        ],
    }
)
