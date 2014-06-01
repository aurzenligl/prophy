import os
import sys
import argparse

def readable_dir(string):
    """
    Checks path to directory in string whether exist
        :param string: path to directory
        :return: the same string if directory exist
    """
    if not os.path.isdir(string):
        raise argparse.ArgumentTypeError("%s directory not found" % string)
    return string

def readable_file(string):
    """
    Checks path to file in string whether exist
        :param string: path to file
        :return: the same string if file exist
    """
    if not os.path.isfile(string):
        raise argparse.ArgumentTypeError("%s file not found" % string)
    return string

def parse_options():
    """
    Parse startup options
        - include_dirs file path to parse
        --patch path to file with patch rules
        --python_out directory, where we want save output python file
    """
    class ArgumentParser(argparse.ArgumentParser):
        def error(self, message):
            self.exit(1, '%s: error: %s\n' % (self.prog, message))

    parser = ArgumentParser(description = 'Isar/sack compiler.')

    group = parser.add_mutually_exclusive_group(required = True)
    group.add_argument('--isar', action = 'store_true')
    group.add_argument('--sack', action = 'store_true')

    parser.add_argument('-I',
                        dest = 'include_dirs',
                        type = readable_dir,
                        action = 'append',
                        default = [],
                        help = 'include directories')

    parser.add_argument('--patch',
                        type = readable_file,
                        help = 'patch file')

    parser.add_argument('--python_out',
                        type = readable_dir,
                        help = 'python output directory')

    parser.add_argument('input_files',
                        type = readable_file,
                        nargs = '+',
                        help = 'input file')

    return parser.parse_args()
