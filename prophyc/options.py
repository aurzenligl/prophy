from optparse import OptionParser
import os


class MyOptionParser(OptionParser):
    def error(self, msg):
        pass

def getOptions():
    parser = MyOptionParser()
    parser.add_option("--input_path", help="input direcotry", type="string", action="store", dest="in_path")
    parser.add_option("--output_path", help="output director", type="string", action="store", dest='out_path',
            default = os.path.join('templates','generated'))
    parser.add_option("--in_format", help="input format ISAR/SACK", type="string", action="store",
            dest="in_format", default="ISAR")
    parser.add_option("--out_format", help="output format: python", type="string", action="store", dest="out_format",
            default="python")
    return parser.parse_args()

if __name__ == "__main__":
    pass
