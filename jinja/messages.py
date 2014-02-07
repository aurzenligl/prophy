from jinja2 import Environment, FileSystemLoader,Template
import os
from xml.dom import minidom
from collections import OrderedDict

import options

#FIME: Turn ON "show whitespace" in IDE, and fix all spaces to tabs. If interpreter got an error in indentation you'll never find it.
# In LOM we use spaces insed of tabs

class Parser(object):

    tmp_dict=OrderedDict()
    typedef_dict={}
    enum_dict={}
    constant_dict={}
    files=[]

    def __init__(self,xml_dir_path):
        self.tree_files=[]
        self.xml_dir = xml_dir_path
        self.script_dir=os.path.dirname(os.path.realpath(__file__)) # FIXME: What is this variable?
        self.set_files_to_parse()
        self.open_files()

    def open_files(self):
        for x in self.files:
            self.tree_files.append(self.open_file(x))

    def delete_old_files(self,files):
        for f in files:
            os.remove(f)

    def open_file(self,file):
        file_dir=os.path.join(self.xml_dir,file)
        dom_tree= minidom.parse(file_dir)
        return dom_tree

    def set_files_to_parse(self):
        all_files=os.listdir(self.xml_dir)
        for f in all_files: # TODO: Think about some error message, now I do not know whether the operation was successful - see the first test
            if f.endswith('.xml'):
                self.files.append(f)
        print self.files

    def struct_parse(self,tree_node,element_name):
        tmp_dict={}
        struct_dict={}
        struct_nodes =tree_node.getElementsByTagName(element_name)
        for p in struct_nodes:
            if p.hasChildNodes():
                name=p.attributes["name"].value
                member=p.getElementsByTagName('member')
                for k in member:
                    tmp_dict=self.checkin_dynamic_fields(k)
                struct_dict[name]=tmp_dict.copy()
                tmp_dict.clear()
        return struct_dict

    def checkin_dynamic_fields(self,k,dyn_dict=OrderedDict()):
        value=k.attributes["type"].value
        if value.startswith('u'):
            value="aprot."+value
        if k.hasChildNodes() and k.getElementsByTagName('dimension'):
            dimension=k.getElementsByTagName('dimension')
            if dimension[0].hasAttribute('size') and not dimension[0].hasAttribute('isVariableSize'):
                dyn_dict[k.attributes["name"].value]=(value,dimension[0].attributes['size'].value)
            elif dimension[0].hasAttribute('isVariableSize'):
                if dimension[0].hasAttribute('variableSizeFieldType') and dimension[0].hasAttribute('variableSizeFieldName'):
                    dyn_dict[k.attributes["name"].value]=(value,dimension[0].attributes['size'].value,dimension[0].attributes['variableSizeFieldType'].value,dimension[0].attributes['variableSizeFieldName'].value)
                elif dimension[0].hasAttribute('variableSizeFieldType') and not dimension[0].hasAttribute('variableSizeFieldName'):
                    dyn_dict[k.attributes["name"].value]=(value,dimension[0].attributes['size'].value,dimension[0].attributes['variableSizeFieldType'].value,"blabla ba")
                elif dimension[0].hasAttribute('variableSizeFieldName') and not dimension[0].hasAttribute('variableSizeFieldType'):
                    dyn_dict[k.attributes["name"].value]=(value,dimension[0].attributes['size'].value,
                        'TNumberOfItems',dimension[0].attributes['variableSizeFieldName'].value)
        else:
            dyn_dict[k.attributes["name"].value]=(value)
        return dyn_dict

    def enum_parse(self,tree_node):
        tmp_dict={}
        enum_dict={}
        enum_nodes=tree_node.getElementsByTagName('enum')
        for enum_element in enum_nodes:
            name=enum_element.attributes["name"].value
            member=enum_element.getElementsByTagName('enum-member')
            for member_enum_element in member:
                value=member_enum_element.getAttribute('value')
                tmp_dict[member_enum_element.attributes["name"].value]=value
            enum_dict[name]=tmp_dict.copy()
            tmp_dict.clear()
        return enum_dict

    def typedef_parse(self,tree_node):
        typedef_dict={}
        typedefNodes=tree_node.getElementsByTagName('typedef')
        for typedef_element in typedefNodes:
            if typedef_element.hasAttribute("type"):
                typedef_dict[typedef_element.attributes["name"].value]=typedef_element.attributes["type"].value
        return typedef_dict

    def constant_parse(self,tree_node, constant_dict={}):
        constant_nodes=tree_node.getElementsByTagName('constant')
        for constant_element in constant_nodes:
            if constant_element.hasAttribute("value"):
                constant_dict[constant_element.attributes["name"].value]=constant_element.attributes["value"].value
        return constant_dict

    def get_include(self, tree_node):
            include_dict = {}
            include_nodes = tree_node.getElementsByTagName("xi:include")
            for include_element in include_nodes:
                if include_element.hasAttribute("href"):
                    include_dict[include_element.attributes["href"].value] = include_element.attributes["xpath"].value
            return include_dict

    def parsing_xml_files(self):
        for tree_node in self.tree_files:
            self.constant_parse(tree_node)
            self.typedef_parse(tree_node)
            self.enum_parse(tree_node)
            self.struct_parse(tree_node,"message")
            self.struct_parse(tree_node,"struct")
            self.get_include(tree_node)

if __name__ == "__main__":
    options,args = options.getOptions()
    xml_path=options.isar_path
    parser=Parser(xml_path)
    parser.parsing_xml_files()

