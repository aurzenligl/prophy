from optparse import OptionParser


def getOptions():
    parser = OptionParser()
    parser.add_option("-i", "--isar_path", help="path to isar dir", type="string", action="store", dest="isar_path", default=".")
    parser.add_option("-o", "--output", help="output format", type="string", action="store", dest='output',
    default='python')
    return parser.parse_args()

if __name__ == "__main__":
    pass
