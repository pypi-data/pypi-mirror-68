# Copyright (c) 2019 Toyota Research Institute

from setuptools import setup, find_packages

DESCRIPTION = "a module that supports an event-sourced system of tracking parameterizations of methods."
LONG_DESCRIPTION = """
taburu (after テーブル) is a module for using hashed arrays as parameter tables
developed by the
[Toyota Research Institute's AMDD division](http://www.tri.global/accelerated-materials-design-and-discovery/).

It's primary purpose is to use event sourcing and hashed parameter tables
to ensure that prior methods can be accounted for when doing new experiments.
"""
setup(
    name='taburu',
    version="2020.5.9",
    packages=find_packages(),
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    url='https://github.com/TRI-AMDD/taburu',
    license='Apache',
    author='joseph.montoya',
    author_email='joseph.montoya@tri.global',
    maintainer='joseph.montoya',
    maintainer_email='joseph.montoya@tri.global',
    install_requires=["monty>=3.0.2",
                      "indexed==1.0.0",
                      "tqdm>=4.46.0",
                      ],
    classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: Apache Software License",
          "Operating System :: OS Independent",
    ],
)