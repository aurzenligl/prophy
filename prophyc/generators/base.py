import os
from prophyc import model


class GenerateError(Exception):
    pass


def _write_file(file_path, string):
    with open(file_path, "w") as f:
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
    def __init__(self, outpu_directory="."):
        self.output_dir = outpu_directory

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
        content = self._process_nodes(nodes, base_name)
        return self._block_post_process(content, base_name, nodes)

    def _process_nodes(self, nodes, base_name):
        def collect():
            previous_node = None
            for node, translated_node in self._nodes_dispatcher(nodes, base_name):
                if self._prepend_newline(previous_node, node):
                    yield '\n'
                yield translated_node + "\n"
                previous_node = node

        return ''.join(collect())

    @classmethod
    def _block_post_process(cls, content, base_name, nodes):
        if cls.block_template:
            return cls.block_template.format(content=content, base_name=base_name, nodes=nodes)
        else:
            return content

    @classmethod
    def _prepend_newline(cls, previous_node, current_node):
        if previous_node:
            is_different_type = type(previous_node) is not type(current_node)
            is_enum_struct_or_union = isinstance(previous_node, (model.Enum, model.Struct, model.Union))
            return is_different_type or is_enum_struct_or_union

    def _nodes_dispatcher(self, nodes, base_name):
        for block_translator_class in self.prerequisite_translators:
            prerequisite_block_translator = block_translator_class()
            translated_block = prerequisite_block_translator(nodes, base_name)
            if translated_block:
                yield "prerequisite block", translated_block

        for node in nodes:
            handler = self._get_translation_handler(node)
            if handler:
                translated_node = handler(node)
                yield node, translated_node

    def _get_translation_handler(self, node):
        if type(node) not in self._translation_methods_map:
            raise GenerateError("Unknown node type: {}".format(type(node).__name__))

        translation_method_name = self._translation_methods_map[type(node)]
        return getattr(self, translation_method_name, None)
