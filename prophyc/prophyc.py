#! /usr/bin/env python

import options
import Parser
import Serializers
import sys
import os

if __name__ == "__main__":
    opts = options.parse_options()

    if opts.isar:
        parser = Parser.XMLParser()

    elif opts.sack:
        sys.exit("Sack header parsing mode not yet implemented")

    if opts.python_out:
        serializer = Serializers.PythonSerializer()

    for input_file in opts.input_files:
        data_holder = parser.parse_xml_file(input_file)
        output = serializer.serialize(data_holder)

        out_filename = os.path.join(opts.python_out, os.path.splitext(os.path.split(input_file)[1])[0] + ".py")
        open(out_filename, "w").write(output)
