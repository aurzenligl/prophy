
from distutils.core import setup

PATHS = [
         "prophy",
         ]

setup(name='prophyc',
      version='1.0',
      description='prophyc library',
      package_dir = {'': 'prophyc'},
      packages=PATHS,
     )