#! /usr/bin/env python

import sys
import os

from . import options
from . import model
from .file_processor import FileProcessor

__version__ = '0.7.8'

class Emit(object):
    @staticmethod
    def warn(msg, location = 'prophyc'):
        sys.stderr.write(location + ': warning: ' + msg + '\n')
    @staticmethod
    def error(msg, location = 'prophyc'):
        sys.exit(location + ': error: ' + msg)

def main():
    opts = options.parse_options(Emit.error)

    if opts.quiet:
        Emit.warn = None

    if opts.version:
        print("prophyc {}".format(__version__))
        sys.exit(0)

    if not opts.input_files:
        Emit.error("missing input file")

    parser = get_parser(opts)
    serializers = get_serializers(opts)
    patcher = get_patcher(opts)

    if not serializers:
        Emit.error("missing output directives")

    def content_parser(*parse_args):
        return parse_content(parser, patcher, *parse_args)

    file_parser = FileProcessor(content_parser, opts.include_dirs)

    for input_file in opts.input_files:
        try:
            nodes = file_parser(input_file)
        except model.ParseError as e:
            sys.exit('\n'.join(('%s: error: %s' % err for err in e.errors)))

        for serializer in serializers:
            basename = get_basename(input_file)
            try:
                serializer.serialize(nodes, basename)
            except model.GenerateError as e:
                Emit.error(str(e))

def get_parser(opts):
    if opts.isar:
        from prophyc.parsers.isar import IsarParser
        return IsarParser(warn = Emit.warn)
    elif opts.sack:
        if not module_exists("clang"):
            Emit.error("sack input requires clang and it's not installed")
        from prophyc.parsers.sack import SackParser
        return SackParser(opts.include_dirs, warn = Emit.warn)
    else:
        from prophyc.parsers.prophy import ProphyParser
        return ProphyParser()

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
    model.cross_reference(nodes, warn = Emit.warn)
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

if __name__ == "__main__":
    main()
