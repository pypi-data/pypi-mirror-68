#!/usr/bin/env python

from setuptools import setup, find_packages

with open("README.md") as f:
    long_desc = f.read()

setup(name="python-algos",
      version=0.14,
      description="A set of bare algorithms",
      long_description=long_desc,
      long_description_content_type="text/markdown", 
      keywords="algorithms graphs directed graphs cyclic kosaraju tarjan",
      author="Evo Williamson",
      author_email="evowilliamson@gmail.com",
      license="GNU General Public License, version 2",
      url="https://github.com/evowilliamson/python-algos",
      packages=find_packages(),
      install_requires=[],
      test_suite="tests",
      classifiers=[
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Topic :: Software Development",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.4",
        "Operating System :: OS Independent"
      ])
