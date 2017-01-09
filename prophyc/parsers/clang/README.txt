This is vendored and modified version of libclang 3.4.2 python bindings.

Changes (in cindex.py.patch):
    - clang is not a package, but subpackage (relative imports)
    - clang offers Python 3 compatibility (2to3)

To update clang bindings (clang tag may be different):

    $ svn export --force http://llvm.org/svn/llvm-project/cfe/tags/RELEASE_342/final/bindings/python/clang .
    $ git citool  # commit unchanged bindings, amend afterwards
    $ patch -p4 < cindex.py.patch
    $ # fix errors
    $ git diff cindex.py > cindex.py.patch
