#!/bin/bash

find_libclangs()
{
    for lib in $(ldconfig -p | grep libclang | awk '{print $4}')
    do
        readlink -f $lib
    done
}

LIBCLANGS=$(find_libclangs | sort -u)
if [ -z "${LIBCLANGS}" ]
then
    echo "libclang not found, won't install python bindings"
    exit 0
fi
echo -e "libclang variants found:\n${LIBCLANGS}"

LIBCLANG=$(basename $(echo "${LIBCLANGS}" | tail -n1))
LIBCLANGVERSION=$(echo "${LIBCLANG}" | grep -Po "libclang-\K[\d.]*(?=.so)")
echo "picking ${LIBCLANG} in version ${LIBCLANGVERSION:-unknown}"

if [ -z ${LIBCLANGVERSION} ]
then
    pip install clang
else
    pip install clang==${LIBCLANGVERSION}
fi

PYCLANGDIR=$(dirname $(python -c "import inspect,clang; print(inspect.getsourcefile(clang))"))

if [ $(python -c 'import sys; print(sys.version_info[0])') == "3" ]
then
    2to3 -w ${PYCLANGDIR}/*.py >& /dev/null
    echo "converted clang/cindex.py with 2to3"
fi

sed -i "s/file = '.*libclang.*so.*'/file = '${LIBCLANG}'/g" ${PYCLANGDIR}/cindex.py
echo "set libclang library default filename to \"${LIBCLANG}\""

#python -c "import sys; print('\n'.join(path for path in sys.path if path))"
#python -c "import sys; print('\n'.join(sys.path))"
#CINDEXFILE=$(python -c "import inspect,clang.cindex; print(inspect.getsourcefile(clang.cindex))")

