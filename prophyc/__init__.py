#! /usr/bin/env python

import sys
import os

from prophyc import options
from prophyc import model
from prophyc.file_processor import FileProcessor

__version__ = '0.5.1dev'

def main():
    opts = options.parse_options(emit_error)

    if opts.version:
        print "prophyc {}".format(__version__)
        sys.exit(0)

    if not opts.input_files:
        emit_error("missing input file")

    parser, parse_error = get_parser(opts)
    serializers = get_serializers(opts)
    patcher = get_patcher(opts)

    if not serializers:
        emit_error("missing output directives")

    def content_parser(*parse_args):
        return parse_content(parser, patcher, *parse_args)

    for input_file in opts.input_files:
        file_parser = FileProcessor(content_parser, opts.include_dirs)
        try:
            nodes = file_parser(input_file)
        except parse_error as e:
            sys.exit('\n'.join(e.errors))

        for serializer in serializers:
            basename = get_basename(input_file)
            try:
                serializer.serialize(nodes, basename)
            except model.GenerateError as e:
                emit_error(e.message)

def get_parser(opts):
    '''Returns parser and parse_error class.'''
    if opts.isar:
        from prophyc.parsers.isar import IsarParser
        return IsarParser(warn = emit_warning), None
    elif opts.sack:
        if not module_exists("clang"):
            emit_error("sack input requires clang and it's not installed")
        from prophyc.parsers.sack import SackParser
        return SackParser(opts.include_dirs), None
    else:
        from prophyc.parsers.prophy import ProphyParser, ParseError
        return ProphyParser(), ParseError

def get_serializers(opts):
    serializers = []
    if opts.python_out:
        from prophyc.generators.python import PythonGenerator
        serializers.append(PythonGenerator(opts.python_out))
    if opts.cpp_out:
        from prophyc.generators.cpp import CppGenerator
        serializers.append(CppGenerator(opts.cpp_out))
    if opts.cpp_full_out:
        from prophyc.generators.cpp_full import CppFullGenerator
        serializers.append(CppFullGenerator(opts.cpp_full_out))
    return serializers

def get_patcher(opts):
    if opts.patch:
        from prophyc import patch
        patches = patch.parse(opts.patch)
        return lambda nodes: patch.patch(nodes, patches)

def parse_content(parser, patcher, *parse_args):
    nodes = parser.parse(*parse_args)
    if patcher:
        patcher(nodes)
    model.topological_sort(nodes)
    model.cross_reference(nodes)
    model.evaluate_kinds(nodes)
    model.evaluate_sizes(nodes)
    return nodes

def get_basename(path):
    return os.path.splitext(os.path.basename(path))[0]

def module_exists(module_name):
    try:
        __import__(module_name)
    except ImportError:
        return False
    else:
        return True

def emit_warning(msg, location = 'prophyc'):
    sys.stderr.write(location + ': warning: ' + msg + '\n')

def emit_error(msg, location = 'prophyc'):
    sys.exit(location + ': error: ' + msg)

if __name__ == "__main__":
    main()
