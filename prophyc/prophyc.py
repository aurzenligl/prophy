#! /usr/bin/env python

import options
import sys
import os
import model_sort

def get_basename(filename):
    return os.path.splitext(os.path.basename(filename))[0]

def main():
    opts = options.parse_options()

    if opts.isar:
        import IsarParser
        parser = IsarParser.IsarParser()
    elif opts.sack:
        import SackParser
        parser = SackParser.SackParser(opts.include_dirs)

    if opts.python_out:
        import PythonSerializer
        serializer = PythonSerializer.PythonSerializer(opts.python_out)
    else:
        sys.exit("Missing output directives")

    for input_file in opts.input_files:
        basename = get_basename(input_file)
        nodes = parser.parse(input_file)
        if opts.patch:
            import patch
            patches = patch.parse(opts.patch)
            patch.patch(nodes, patches)

        model_sort.model_sort(nodes)
        serializer.serialize(nodes, basename)

if __name__ == "__main__":
    main()
