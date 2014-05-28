from setuptools import setup

setup(name = 'prophy',
      packages = ['prophy', 'prophyc'],
      entry_points = {
        'console_scripts': [
            'prophyc = prophyc.prophyc:main']
        },
      version = '0.2.4',
      description = 'Binary data interchange format toolchain',
      author = 'Krzysztof Laskowski',
      author_email = 'krzysztof.laskowski@nsn.com',
      url = "https://pypi.python.org/pypi",
      keywords = ["IDL", "codec", "binary data"],
      classifiers = [
            "Intended Audience :: Developers",
            "Intended Audience :: Telecommunications Industry",
            "Programming Language :: Python",
            "Development Status :: 3 - Alpha",
            "License :: OSI Approved :: MIT License",
            "Operating System :: Unix",
            "Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator",
            "Topic :: Software Development :: Libraries :: Python Modules",
            ]
      )
