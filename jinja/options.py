from optparse import OptionParser


def getOptions():
    parser = OptionParser()
    parser.add_option("-i", "--isar_path", help="path to isar dir", type="string", action="store", dest="isar_path", default=".")
    return parser.parse_args()

if __name__ == "__main__":
    pass