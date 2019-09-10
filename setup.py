#!/usr/bin/env python
from distutils.core import setup

pname = "checkimpcont"
setup(name=pname, version="0.0.3",
      author="Cong Ma",
      author_email="cong.ma@uct.ac.za",
      scripts=["checkimpcont.py"],
      provides=[pname],
      classifiers=["Development Status :: 4 - Beta",
                   "Environment :: Console",
                   "Intended Audience :: Developers",
                   "Operating System :: OS Independent",
                   "Programming Language :: Python",
                   "Programming Language :: Python :: 2.7",
                   "Programming Language :: Python :: 3",
                   "Topic :: Software Development :: Quality Assurance",
                   "Topic :: Text Processing :: Filters",
                   "Topic :: Utilities"])
