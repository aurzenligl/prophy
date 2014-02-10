import messages
from reader import XmlReader
import xml.dom

def test_create_of_parser():
    parser = messages.Parser()


def test_of_opening_files():
    reader =XmlReader(".")
    reader.read_files()

