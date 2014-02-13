import reader

import os
import shutil

def test_of_xml_reader():
    test_dir_name = "xml_test_files"
    shutil.rmtree(test_dir_name, ignore_errors=True)
    os.mkdir(test_dir_name)
    xml_dir_path =  os.path.join(".", test_dir_name)
    document = """\
        <slideshow>
        <title>Demo slideshow</title>
        <slide><title>Slide title</title>
        <point>This is a demo</point>
        <point>Of a program for processing slides</point>
        </slide>

        <slide><title>Another demo slide</title>
        <point>It is important</point>
        <point>To have more than</point>
        <point>one slide</point>
        </slide>
        </slideshow>
        """
    for x in range(0, 10):
        f = open(os.path.join(xml_dir_path, str(x) + ".xml"),"w");
        f.write(document)
        f.close()

    r = reader.XmlReader(xml_dir_path)
    r.read_files()
    assert 10 == len(r.return_tree_files())

def test_of_xml_reader_1():
    test_dir_name = "xml_test_files"
    shutil.rmtree(test_dir_name, ignore_errors=True)
    os.mkdir(test_dir_name)
    xml_dir_path =  os.path.join(".", test_dir_name)
    document = """\
        <slideshow>
        <title>Demo slideshow</title>
        <slide><title>Slide title</title>
        <point>This is a demo</point>
        <point>Of a program for processing slides</point>
        </slide>

        <slide><title>Another demo slide</title>
        <point>It is important</point>
        <point>To have more than</point>
        <point>one slide</point>
        </slide>
        </slideshow>
        """
    for x in range(0, 10):
        f = open(os.path.join(xml_dir_path, str(x) + ".xml"),"w");
        f.write(document)
        f.close()

    r = reader.XmlReader(xml_dir_path)
    assert 10 == len(r.return_tree_files())
