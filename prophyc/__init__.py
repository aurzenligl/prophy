#! /usr/bin/env python

import sys
import os

from prophyc import options
from prophyc import model_sort

def get_basename(filename):
    return os.path.splitext(os.path.basename(filename))[0]

def main():
    opts = options.parse_options()

    if opts.isar:
        from prophyc.parsers.isar import IsarParser
        parser = IsarParser()
    elif opts.sack:
        from prophyc.parsers.sack import SackParser
        parser = SackParser(opts.include_dirs)

    serializers = []
    if opts.python_out:
        from prophyc.generators.python import PythonGenerator
        serializers.append(PythonGenerator(opts.python_out))
    if opts.cpp_out:
        from prophyc.generators.cpp import CppGenerator
        serializers.append(CppGenerator(opts.cpp_out))

    if not serializers:
        sys.exit("Missing output directives")

    for input_file in opts.input_files:
        basename = get_basename(input_file)
        nodes = parser.parse(input_file)
        if opts.patch:
            from prophyc import patch
            patches = patch.parse(opts.patch)
            patch.patch(nodes, patches)

        model_sort.model_sort(nodes)
        for serializer in serializers:
            serializer.serialize(nodes, basename)

if __name__ == "__main__":
    main()
