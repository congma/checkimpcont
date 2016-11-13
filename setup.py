#!/usr/bin/env python
from distutils.core import setup

pname = "checkimpcont"
setup(name=pname, version="0.0.1",
      author="Cong Ma",
      author_email="cong.ma@obspm.fr",
      scripts=["checkimpcont.py"],
      provides=[pname])
