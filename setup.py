
from distutils.core import setup

PATHS = [
         "Messages",
         "message_object_tests",
         "protophy",
         "templates",
         "templates\generated"]

setup(name='protophy',
      version='1.0',
      description='ute_dspi library',
      package_dir = {'': 'ute_dspi'},
      packages=PATHS,
     )