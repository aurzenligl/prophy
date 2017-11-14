#! /usr/bin/env python

import sys
import os

from . import options
from . import model
from .file_processor import FileProcessor
from contextlib import contextmanager

__version__ = '1.1.1'

class ProphycError(Exception):
    pass

class Emit(object):
    def __init__(self):
        self.quiet = False

    def warn(self, msg, location='prophyc'):
        if not self.quiet:
            sys.stderr.write(location + ': warning: ' + msg + '\n')

    def error(self, msg, location='prophyc'):
        raise ProphycError(location + ': error: ' + msg)

def main(args):
    emit = Emit()
    opts = options.parse_options(emit.error, args)

    emit.quiet = opts.quiet

    if opts.version:
        print("prophyc {}".format(__version__))
        return

    if not opts.input_files:
        emit.error("missing input file")

    serializers = get_serializers(opts)
    patcher = get_patcher(opts)

    if not serializers:
        emit.error("missing output directives")

    supplementary_nodes = []
    if opts.isar_includes:
        if not opts.sack:
            emit.error('Isar defines inclusion is supported only in "sack" compilation mode.')

        isar_parser = get_isar_parser(emit)
        model_parser = ModelParser(isar_parser, patcher, emit)
        file_parser = FileProcessor(model_parser, opts.include_dirs)

        for input_file in opts.isar_includes:
            with error_on_exception(emit):
                include_nodes = file_parser(input_file)
            basename = get_basename(input_file)
            supplementary_nodes.append(model.Include(basename, include_nodes))

        for include_name, include_nodes in flatten_included_defs(supplementary_nodes):
            generate_target_files(emit, serializers, include_name, include_nodes)

    parser = get_target_parser(emit, opts, supplementary_nodes)
    model_parser = ModelParser(parser, patcher, emit)
    file_parser = FileProcessor(model_parser, opts.include_dirs)

    for input_file in opts.input_files:
        with error_on_exception(emit):
            nodes = file_parser(input_file)
        generate_target_files(emit, serializers, get_basename(input_file), nodes)

def get_isar_parser(emit):
    from prophyc.parsers.isar import IsarParser
    return IsarParser(warn=emit.warn)

def get_target_parser(emit, opts, supplementary_nodes):
    if opts.isar:
        return get_isar_parser(emit)
    elif opts.sack:
        from prophyc.parsers.sack import SackParser
        status = SackParser.check()
        if not status:
            emit.error(status.error)
        return SackParser(opts.include_dirs, warn=emit.warn, include_tree=supplementary_nodes)
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

class ModelParser():
    def __init__(self, parser, patcher, emit):
        self.parser = parser
        self.patcher = patcher
        self.emit = emit

    def __call__(self, *parse_args):
        nodes = self.parser.parse(*parse_args)
        if self.patcher:
            self.patcher(nodes)
        model.topological_sort(nodes)
        model.cross_reference(nodes, warn=self.emit.warn)
        model.evaluate_kinds(nodes)
        model.evaluate_sizes(nodes, warn=self.emit.warn)
        return nodes

def get_basename(path):
    return os.path.splitext(os.path.basename(path))[0]

def flatten_included_defs(supple_nodes):
    def get_nodes_and_names(nodes_list):
        for elem in nodes_list:
            if isinstance(elem, model.Include):
                yield elem
                for sub_elem in get_nodes_and_names(elem.nodes):
                    yield sub_elem
    """ pass trough a dictionary to avoid duplicates """
    return tuple(dict(get_nodes_and_names(supple_nodes)).items())

def generate_target_files(emit, serializers, basename, nodes):
    for serializer in serializers:
        try:
            serializer.serialize(nodes, basename)
        except model.GenerateError as e:
            emit.error(str(e))

@contextmanager
def error_on_exception(emit):
    try:
        yield
    except model.ParseError as e:
        emit.error('\n'.join(('%s: error: %s' % err for err in e.errors)))
