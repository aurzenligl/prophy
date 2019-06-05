#! /usr/bin/env python

import os
import sys
from contextlib import contextmanager

from . import model
from . import options
from .file_processor import FileProcessor
from .generators.base import GenerateError

__version__ = '1.2.3'


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
        return {}

    if not opts.input_files:
        emit.error("missing input file")

    if opts.isar_includes and not opts.sack:
        emit.error('Isar defines inclusion is supported only in "sack" compilation mode.')

    serializers = get_serializers(opts)

    if not serializers and not opts.void_out:
        emit.error("missing output directives")

    patcher = get_patcher(opts.patch)
    supplementary_nodes = create_supplements(emit, opts.isar_includes, opts.include_dirs, patcher)

    model_nodes = dict(flatten_included_defs(supplementary_nodes))

    source_parser = get_target_parser(emit, opts, supplementary_nodes)
    model_parser = model.ModelParser(source_parser, patcher, emit)
    file_processor_ = FileProcessor(model_parser, opts.include_dirs)

    for input_file in opts.input_files:
        with error_on_exception(emit):
            nodes = file_processor_(input_file)
            basename = get_basename(input_file)
            model_nodes[basename] = nodes

    generate_target_files(emit, serializers, model_nodes)

    return model_nodes


def create_supplements(emit, isar_includes, include_dirs, patcher):
    isar_parser = get_isar_parser(emit)
    model_parser = model.ModelParser(isar_parser, patcher, emit)
    file_parser = FileProcessor(model_parser, include_dirs)
    supplementary_nodes = []
    for input_file in isar_includes:
        with error_on_exception(emit):
            include_nodes = file_parser(input_file)
        basename = get_basename(input_file)
        supplementary_nodes.append(model.Include(basename, include_nodes))
    return supplementary_nodes


def get_target_parser(emit, opts, supplementary_nodes):
    if opts.isar:
        return get_isar_parser(emit)
    elif opts.sack:
        return get_sack_parser(emit, supplementary_nodes, opts.include_dirs)
    else:
        from prophyc.parsers.prophy import ProphyParser
        return ProphyParser()


def get_isar_parser(emit):
    from prophyc.parsers.isar import IsarParser
    return IsarParser(warn=emit.warn)


def get_sack_parser(emit, supplementary_nodes, sack_include_dirs):
    from prophyc.parsers.sack import SackParser
    status = SackParser.check()
    if not status:
        emit.error(status.error)
    return SackParser(sack_include_dirs, warn=emit.warn, include_tree=supplementary_nodes)


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
    if opts.prophy_out:
        from prophyc.generators.prophy import SchemaGenerator
        serializers.append(SchemaGenerator(opts.prophy_out))
    return serializers


def get_patcher(patch_file_path):
    if patch_file_path:
        from prophyc import patch
        patches = patch.parse(patch_file_path)
        return lambda nodes: patch.patch(nodes, patches)


def get_basename(path):
    return os.path.splitext(os.path.basename(path))[0]


def flatten_included_defs(supple_nodes):
    def get_nodes_and_names(nodes_list):
        for elem in nodes_list:
            if isinstance(elem, model.Include):
                yield elem.name, elem.members
                for sub_elem in get_nodes_and_names(elem.members):
                    yield sub_elem

    """ pass trough a dictionary to avoid duplicates """
    return tuple(dict(get_nodes_and_names(supple_nodes)).items())


def generate_target_files(emit, serializers, model_nodes):
    for basename, nodes in model_nodes.items():
        for serializer in serializers:
            try:
                serializer.serialize(nodes, basename)
            except GenerateError as e:
                emit.error(str(e))


@contextmanager
def error_on_exception(emit):
    try:
        yield
    except model.ParseError as e:
        emit.error('\n'.join(('%s: error: %s' % err for err in e.errors)))
