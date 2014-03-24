#! /usr/bin/env python

import options
import Parser
import Serializers
import sys
import os

def get_basename(filename):
    return os.path.splitext(os.path.basename(filename))[0]

if __name__ == "__main__":
    opts = options.parse_options()

    if opts.isar:
        parser = Parser.XMLParser()
    elif opts.sack:
        sys.exit("Sack header parsing mode not yet implemented")

    if opts.python_out:
        serializer = Serializers.PythonSerializer(opts.python_out)

    for input_file in opts.input_files:
        basename = get_basename(input_file)
        data_holder = parser.parse(input_file)
        serializer.serialize(data_holder, basename)
