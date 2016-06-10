import os
import argparse

def readable_dir(string):
    if not os.path.isdir(string):
        raise argparse.ArgumentTypeError("%s directory not found" % string)
    return string

def readable_file(string):
    if not os.path.isfile(string):
        raise argparse.ArgumentTypeError("%s file not found" % string)
    return string

def parse_options(emit_error):
    class ArgumentParser(argparse.ArgumentParser):
        def error(self, message):
            emit_error(message)

    parser = ArgumentParser('prophyc',
                            description = ('Parse input files and generate '
                                           'output based on options given.'))

    parser.add_argument('input_files',
                        metavar = 'INPUT_FILE',
                        type = readable_file,
                        nargs = '*',
                        help = ('Prophy language, C++ or isar xml files with definitions of prophy '
                                'messages. By default prophy language is assumed.'))

    group = parser.add_mutually_exclusive_group()
    group.add_argument('--isar',
                       action = 'store_true',
                       help = 'Parse input files as isar xml.')
    group.add_argument('--sack',
                       action = 'store_true',
                       help = 'Parse input files as sack C++.')

    parser.add_argument('-I', '--include_dir',
                        metavar = 'DIR',
                        dest = 'include_dirs',
                        type = readable_dir,
                        action = 'append',
                        default = [],
                        help = ('Add the directory to the list of directories to be '
                                'searched for included files.'))

    parser.add_argument('-p', '--patch',
                        metavar = 'FILE',
                        type = readable_file,
                        help = ("File with instructions changing definitions of prophy "
                                "messages after parsing. It's needed in sack and isar "
                                "modes, since C++ and isar xml are unable to express "
                                "all prophy features."))

    parser.add_argument('--python_out',
                        metavar = 'OUT_DIR',
                        type = readable_dir,
                        help = 'Generate Python source files.')

    parser.add_argument('--cpp_out',
                        metavar = 'OUT_DIR',
                        type = readable_dir,
                        help = 'Generate C++ simple POD-based codec header and source files.')

    parser.add_argument('--cpp_full_out',
                        metavar = 'OUT_DIR',
                        type = readable_dir,
                        help = 'Generate C++ full object-based codec header and source files.')

    parser.add_argument('--version',
                        action = 'store_true',
                        help = 'Show version information and exit.')

    parser.add_argument('--quiet',
                        action = 'store_true',
                        help = 'Suppress warnings prints.')

    return parser.parse_args()
