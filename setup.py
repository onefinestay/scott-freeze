from setuptools import setup
import os

def read_file(*paths):
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, *paths)) as f:
        return f.read()

long_description = read_file('README.rst')


setup(
    name='scott-freeze',
    version='0.1',
    description='Utility for managing requirements files',
    long_description=long_description,
    author='onefinestay',
    author_email='engineering@onefinestay.com',
    url='http://github.com/onefinestay/scott-freeze',
    py_modules=['scott_freeze'],
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
        "Intended Audience :: Developers",
    ]
)
