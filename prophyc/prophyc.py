#! /usr/bin/env python

import Serializers
import options
import Parser
import sys
import os

if __name__ == "__main__":
    opts = options.parse_options()

    if opts.python_out:
        for input_file in opts.input_files:
            data_holder = Parser.XMLParser().parse_xml_file(input_file)
            ps = Serializers.PythonSerializer()
            o = ps.serialize(data_holder)

            out_filename = os.path.splitext(input_file.name)[0] + ".py"
            open(out_filename, "w").write(o)
    else:
        print "Missing output directives."