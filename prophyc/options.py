import argparse

def parse_options():
    parser = argparse.ArgumentParser(description = 'Isar/sack compiler.')
    parser.add_argument('input_files',
                        type = file,
                        nargs = '+',
                        help = 'input file')
    parser.add_argument('--python_out',
                        help = 'python output directory')
    return parser.parse_args()
