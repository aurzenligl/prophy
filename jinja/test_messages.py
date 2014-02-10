import messages
import xml.dom

def test_create_of_parser():
    parser = messages.Parser(".")


def test_of_opening_files():
    parser = messages.Parser(".")
    parser.open_files()

def test_of_constant_sorting():
    l = ["CONST_A = 5", "CONST_B = CONST_A + 15"]

    example = """<constant comment="Number of different measurement groups in MAC" name="MAX_MEAS_GROUP_TYPE_ID_MAC" value="MAX_MEAS_GROUP_TYPE_ID"/>
    <constant forceGeneration="true" name="MAX_MEAS_GROUP_TYPE_ID" value="22"/>"""

    tree = xml.dom.minidom.parseString(example)
    assert l = messages.__constant_sorter(tree)