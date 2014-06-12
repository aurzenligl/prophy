from setuptools import setup

long_description = open('README.rst').read()

setup(name = 'prophy',
      packages = ['prophy', 'prophyc'],
      entry_points = {
          'console_scripts': [
              'prophyc = prophyc.prophyc:main'
          ]
      },
      version = '0.2.5',
      description = 'prophy: fast data interchange format toolchain',
      long_description = long_description,
      author = 'Krzysztof Laskowski',
      author_email = 'krzysztof.laskowski@nsn.com',
      url = "https://github.com/aurzenligl/prophy",
      license = 'MIT license',
      keywords = "IDL codec binary data",
      classifiers = [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Developers",
            "Intended Audience :: Telecommunications Industry",
            "License :: OSI Approved :: MIT License",
            "Operating System :: Unix",
            "Operating System :: Microsoft :: Windows",
            "Programming Language :: Python :: 2.7",
            "Topic :: Utilities",
            "Topic :: Software Development :: Libraries",
            "Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator",
      ],
      zip_safe = False
)
