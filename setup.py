from setuptools import setup, find_packages

long_description = open('README.rst').read()

setup(
    name = 'prophy',
    version = '1.1.1',
    author = 'Krzysztof Laskowski',
    author_email = 'krzysztof.laskowski@nokia.com',
    maintainer = 'Krzysztof Laskowski',
    maintainer_email = 'krzysztof.laskowski@nokia.com',
    license = 'MIT license',
    url = 'https://github.com/aurzenligl/prophy',
    description = 'prophy: fast serialization protocol',
    long_description = long_description,
    packages = find_packages(),
    requires = ['ply'],
    install_requires = ['ply'],
    keywords = 'idl codec binary data protocol compiler',
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Telecommunications Industry',
        'Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator',
        'Topic :: Software Development :: Code Generators',
        'Topic :: Software Development :: Compilers',
        'Topic :: Software Development :: Embedded Systems',
        'Topic :: Software Development :: Testing',
        'Topic :: Software Development :: Libraries',
        'Topic :: Utilities',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: C++',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
    ],
    entry_points = {
        'console_scripts': [
            'prophyc = prophyc.__main__:entry_main'
        ],
    },
)
