#!/usr/bin/env python
from setuptools import setup, find_packages
from codecs import open  # To use a consistent encoding
from os import path


setup_dir = path.dirname(path.abspath(__file__))
with open(path.join(setup_dir, 'README.rst'), encoding='utf-8') as handle:
    long_description = handle.read()


setup(
    name='scott-freeze',
    version='0.1',
    description='Utility for managing requirements files',
    long_description=long_description,
    author='onefinestay',
    author_email='engineering@onefinestay.com',
    url='http://github.com/onefinestay/scott-freeze',
    packages=find_packages(exclude=['test', 'test.*']),
    entry_points={
        'console_scripts': [
            'scott-freeze=scott_freeze:main',
        ],
    },
    zip_safe=False,
    license='Apache License, Version 2.0',
    classifiers=[
        "Programming Language :: Python",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 2.7",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Intended Audience :: Developers",
    ]
)
