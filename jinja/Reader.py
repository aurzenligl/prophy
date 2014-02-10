

class Reader(object):
    @staticmethod
    def readFile(file_name):
        f = open(file_name, "r")
        return f.read()