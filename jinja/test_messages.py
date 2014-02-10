import messages


def test_create_of_parser():
    parser = messages.Parser(".")


def test_of_opening_files():
    parser = messages.Parser(".")
    parser.open_files()