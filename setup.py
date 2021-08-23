#!/usr/bin/env python

from setuptools import setup, find_packages
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pygustus',
    version='0.7.0',
    description='Python wrapper for AUGUSTUS.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Daniel Honsel',
    author_email='dhonsel@cs.uni.goettingen.de',
    url='https://github.com/Gaius-Augustus/pygustus',
    download_url='https://github.com/Gaius-Augustus/pygustus/zipball/master',
    packages=find_packages(),
    package_data={'pygustus': ['options/parameters.json', 'config.json']},
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: POSIX :: Linux",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
    ],
    install_requires=[
        "biopython",
    ],
)
