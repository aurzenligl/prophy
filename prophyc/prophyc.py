#! /usr/bin/env python

import writer
import Serializers
import options
import reader
import Parser
import sys
import os

if __name__ == "__main__":
    options, args = options.getOptions()
    reader = reader.get_reader()
    parser = Parser.get_parser()

    data_holder = parser.parsing_xml_files(reader.xml_tree)
    w = writer.get_writer(reader.basename + ".py")
    ps = Serializers.PythonSerializer()
    o = ps.serialize(data_holder)
    w.write_to_file(o)
