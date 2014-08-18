#! /usr/bin/env python

import sys
import os

from prophyc import options

__version__ = '0.4.1'

def get_basename(filename):
    return os.path.splitext(os.path.basename(filename))[0]

def module_exists(module_name):
    try:
        __import__(module_name)
    except ImportError:
        return False
    else:
        return True

def main():
    opts = options.parse_options()

    if opts.version:
        print "prophyc {}".format(__version__)
        sys.exit(0)

    if not opts.input_files:
        sys.exit("prophyc: error: missing input file")

    if opts.isar:
        from prophyc.parsers.isar import IsarParser
        parser = IsarParser()
        parse_error = None
    elif opts.sack:
        if not module_exists("clang"):
            sys.exit("Sack input requires clang and it's not installed")
        from prophyc.parsers.sack import SackParser
        parser = SackParser(opts.include_dirs)
        parse_error = None
    else:
        from prophyc.parsers.prophy import ProphyParser, ParseError
        parser = ProphyParser()
        parse_error = ParseError

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
        try:
            nodes = parser.parse(input_file)
        except parse_error as e:
            sys.exit('\n'.join(e.errors))

        if opts.patch:
            from prophyc import patch
            patches = patch.parse(opts.patch)
            patch.patch(nodes, patches)
        model.topological_sort(nodes)
        model.cross_reference(nodes)
        model.evaluate_kinds(nodes)

        for serializer in serializers:
            basename = get_basename(input_file)
            serializer.serialize(nodes, basename)

if __name__ == "__main__":
    main()
