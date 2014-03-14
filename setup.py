
from distutils.core import setup

PATHS = [
         "protophy",
         "templates",
         ]

setup(name='protophy',
      version='1.0',
      description='ute_dspi library',
      package_dir = {'': 'ute_dspi'},
      packages=PATHS,
     )