from optparse import OptionParser


class MyOptionParser(OptionParser):
    def error(self, msg):
        pass

def getOptions():
    parser = MyOptionParser()
    parser.add_option("-i", "--isar_path", help="path to isar dir", type="string", action="store", dest="isar_path", default=".")
    parser.add_option("-o", "--output", help="output format", type="string", action="store", dest='output',
    default='python')
    return parser.parse_args()

if __name__ == "__main__":
    pass
