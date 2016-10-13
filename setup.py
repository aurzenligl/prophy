from setuptools import setup, find_packages

long_description = open('README.rst').read()

setup(name = 'prophy',
      packages = find_packages(),
      requires = ['ply'],
      install_requires = ['ply'],
      include_package_data = True,
      entry_points = {
          'console_scripts': [
              'prophyc = prophyc:main'
          ]
      },
      version = '0.7.8',
      description = 'prophy: fast serialization protocol',
      long_description = long_description,
      author = 'Krzysztof Laskowski',
      author_email = 'krzysztof.laskowski@nokia.com',
      url = "https://github.com/aurzenligl/prophy",
      license = 'MIT license',
      keywords = "idl codec binary data protocol compiler",
      classifiers = [
            "Development Status :: 4 - Beta",
            "Intended Audience :: Developers",
            "Intended Audience :: Telecommunications Industry",
            "License :: OSI Approved :: MIT License",
            "Operating System :: Unix",
            "Operating System :: Microsoft :: Windows",
            "Programming Language :: Python :: 2.7",
            "Programming Language :: Python :: 3.4",
            "Programming Language :: C++",
            "Topic :: Utilities",
            "Topic :: Software Development :: Libraries",
            "Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator",
      ],
      zip_safe = False
)
