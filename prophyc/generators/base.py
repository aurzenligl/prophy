import os
from prophyc import model


class GenerateError(Exception):
    pass


class GeneratorBase(object):
    file_translators = {}

    def __init__(self, output_dir="."):
        self.output_dir = output_dir

    def serialize(self, nodes, base_name):
        self.check_nodes(nodes)

        for extension, translator_class in self.file_translators.items():
            translator = translator_class()
            contents = translator(nodes, base_name)
            file_path = self.make_path(base_name, extension)
            self.write_file(file_path, contents)

    def make_path(self, base_name, extension):
        assert extension.startswith(".")
        file_path = os.path.join(self.output_dir, base_name + extension)
        return file_path

    def check_nodes(self, nodes):
        "No check performed."

    def write_file(self, file_path, string):
        with open(file_path, "w") as f:
            f.write(string)


class TranslatorBase(object):
    block_template = "{content}"
    block_translators = []
    _translation_methods_map = {
        model.Constant: "_translate_constant",
        model.Enum: "_translate_enum",
        model.Include: "_translate_include",
        model.Struct: "_translate_struct",
        model.Typedef: "_translate_typedef",
        model.Union: "_translate_union",
    }

    def __call__(self, nodes, base_name):
        content = self.process_nodes(nodes, base_name)
        content = self.block_post_process(content, base_name, nodes)
        return content

    def process_nodes(self, nodes, base_name):
        return ''.join(self._nodes_dispatcher(nodes, base_name))

    def block_post_process(self, content, base_name, nodes):
        return self.block_template.format(content=content, base_name=base_name, nodes=nodes)

    def prepend_newline(self, previous_node, current_node):
        is_different_type = type(previous_node) is not type(current_node)
        is_enum_struct_or_union = isinstance(previous_node, (model.Enum, model.Struct, model.Union))

        if previous_node:
            return is_different_type or is_enum_struct_or_union

    def _nodes_dispatcher(self, nodes, base_name):
        for block_translator_class in self.block_translators:
            block_translator = block_translator_class()
            yield block_translator(nodes, base_name)

        previous_node = None
        for node in nodes:
            handler = self._get_translation_handler(node)
            if handler:
                translated_node = handler(node)

                if self.prepend_newline(previous_node, node):
                    yield '\n'

                yield translated_node + '\n'
                previous_node = node

    def _get_translation_handler(self, node):
        translation_method_name = self._translation_methods_map.get(type(node), None)
        if translation_method_name:
            return getattr(self, translation_method_name, None)
