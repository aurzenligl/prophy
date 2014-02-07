from optparse import OptionParser

parser = OptionParser()

parser.add_option("-i", "--isar_path", help="path to isar dir", type="string", action="store", dest="isar_path")


print parser.parse_args()