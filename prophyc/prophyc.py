#! /usr/bin/env python

import Serializers
import options
import Parser
import sys
import os

if __name__ == "__main__":
    opts = options.parse_options()
    if opts.sack:
        sys.exit("Sack header parsing mode not yet implemented")

    if opts.python_out:
        for input_file in opts.input_files:
            data_holder = Parser.XMLParser().parse_xml_file(input_file)
            ps = Serializers.PythonSerializer()
            o = ps.serialize(data_holder)

            out_filename = os.path.join(opts.python_out, os.path.splitext(os.path.split(input_file)[1])[0] + ".py")
            open(out_filename, "w").write(o)
