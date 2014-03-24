#! /usr/bin/env python

import Serializers
import options
import Parser
import sys
import os

if __name__ == "__main__":
    opts = options.parse_options()

    if not opts.input_files:
        print "Missing input file."
        sys.exit(1)

    if opts.python_out:
        if not os.path.exists(opts.python_out):
            print "%s: No such directory." % opts.python_out
            sys.exit(1)

        for input_file in opts.input_files:
            data_holder = Parser.XMLParser().parse_xml_file(input_file)
            ps = Serializers.PythonSerializer()
            o = ps.serialize(data_holder)

            out_filename = os.path.join(opts.python_out, os.path.splitext(os.path.split(input_file.name)[1])[0] + ".py")
            open(out_filename, "w").write(o)
        sys.exit(0)
    else:
        print "Missing output directives."
        sys.exit(1)
