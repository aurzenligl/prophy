import codecs
import os

from prophyc import model


class GenerateError(Exception):
    pass


def _write_file(file_path, string):
    with codecs.open(file_path, "w", encoding="utf-8") as f:
        f.write(string)


def _make_path(output_dir, base_name, extension):
    assert extension.startswith(".")
    assert os.path.isdir(output_dir), "Output directory %s doesn't exist." % output_dir
    return os.path.join(output_dir, base_name + extension)


class GeneratorAbc(object):
    """
        Generator class implements one language that model is translated to.
        Generator needs to map at least one translator to its file extension in top_level_translators.
        And to implement check_nodes method.
    """
    top_level_translators = {}

    def check_nodes(self, nodes):
        """
            Before a model is translated to given language it needs to be checked if it conforms to given
            language requirements. It's a place to raise exceptions if needed.
        """


class GeneratorBase(GeneratorAbc):
    def __init__(self, output_directory="."):
        self.output_dir = output_directory

    def serialize(self, nodes, base_name):
        self.check_nodes(nodes)

        for extension, translator_type in self.top_level_translators.items():
            file_path = _make_path(self.output_dir, base_name, extension)
            translator = translator_type()
            file_content = translator(nodes, base_name)
            _write_file(file_path, file_content)


class TranslatorAbc(object):
    """
        A translator represents block of content in generated file, (e.g. includes block, constants block, etc..).
        Translator class can use sub-translator classes as prerequisites (prerequisite_translators).
        After finishing nodes processing - block_template is applied on generated content (_block_post_process).

        To enable translation of given node type just implement a corresponding method from
        _translation_methods_map. The method has to take a single node and return a string with translation result.

        Dispatcher will skip translation of nodes of types that have no translation implemented.
        E.g. if there is no method called `translate_typedef`, typedef model nodes will
        be not translated by given translator class.
    """
    prerequisite_translators = []
    block_template = None


class TranslatorBase(TranslatorAbc):
    _translation_methods_map = {
        model.Constant: "translate_constant",
        model.Enum: "translate_enum",
        model.Include: "translate_include",
        model.Struct: "translate_struct",
        model.Typedef: "translate_typedef",
        model.Union: "translate_union",
    }

    def __call__(self, nodes, base_name):
        nodes = self._move_includes_to_front(nodes)
        content = self._process_nodes(nodes, base_name)
        return self._block_post_process(content, base_name, nodes)

    def _process_nodes(self, nodes, base_name):
        render = ""
        previous_node_type = None
        for node_type_name, translated_node in self._nodes_dispatcher(nodes, base_name):
            lines_splitter = self._make_lines_splitter(previous_node_type, node_type_name)
            if translated_node:
                render += lines_splitter + translated_node

            previous_node_type = node_type_name

        if nodes and render:
            render += "\n"
        return render

    @classmethod
    def _block_post_process(cls, content, base_name, nodes):
        if cls.block_template:
            return cls.block_template.format(content=content, base_name=base_name, nodes=nodes)
        else:
            return content

    @classmethod
    def _make_lines_splitter(cls, previous_node_type, current_node_type):
        if not previous_node_type:
            return ""

        if previous_node_type != current_node_type:
            return "\n\n"

        return "\n"

    def _nodes_dispatcher(self, nodes, base_name):
        for block_translator_class in self.prerequisite_translators:
            prerequisite_block_translator = block_translator_class()
            translated_block = prerequisite_block_translator(nodes, base_name)
            if nodes and translated_block:
                last_node_name = type(nodes[-1]).__name__
                yield last_node_name, translated_block

        for node in nodes:
            handler = self._get_translation_handler(node)
            if handler:
                translated_node = handler(node)
                yield type(node).__name__, translated_node

    def _get_translation_handler(self, node):
        translation_method_name = self._translation_methods_map.get(type(node), None)
        assert translation_method_name, "Unknown node type: {}".format(type(node).__name__)
        return getattr(self, translation_method_name, None)

    @staticmethod
    def _move_includes_to_front(nodes):
        includes = []
        others = []
        for node in nodes:
            if isinstance(node, model.Include):
                includes.append(node)
            else:
                others.append(node)
        return includes + others
