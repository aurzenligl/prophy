import pytest

from prophyc.generators import base
from prophyc import model
from prophyc.generators.base import GenerateError


def make_dummy_translation_method(name):
    template = '<{}> [{{content}}]'.format(name)

    def dummy_translation(node):
        return template.format(content=node)
    return dummy_translation


@pytest.fixture
def straigth_generator():

    class EmptyTranslator(base.BlockTranslatorBase):
        pass

    class StraightTranslator(base.BlockTranslatorBase):
        block_template = '''scope {base_name} {{\n{content}\n}} // endscope {base_name}\n'''

        def __init__(self):
            for model_type, translator_name in base.BlockTranslatorBase.translation_methods_map.items():
                method = make_dummy_translation_method(model_type.__name__)
                setattr(self, translator_name, method)

    class StraightGenerator(base.GeneratorBase):
        top_level_translators = {
            '.st': StraightTranslator,
            '.em': EmptyTranslator
        }

    return StraightGenerator


@pytest.fixture
def serialize(mocker, straigth_generator):
    scoper = type('scoper', (), {'writes': {}})

    def write_mock(file_path, file_content):
        scoper.writes.update({file_path: file_content})

    mocker.patch.object(base, '_write_file', side_effect=write_mock)
    mocker.patch.object(base.os.path, 'isdir', return_value=True)

    def process(nodes, base_name='mainer'):
        model.cross_reference(nodes)
        model.evaluate_kinds(nodes)
        model.evaluate_sizes(nodes)
        gen = straigth_generator('fake_out')
        gen.check_nodes(nodes)
        gen.serialize(nodes, base_name)

        return scoper.writes
    return process


TRANSLATION_MODEL_A = []
TRANSLATION_WRITES_A = {
    'fake_out/mainer.em': '',
    'fake_out/mainer.st': 'scope mainer {\n\n} // endscope mainer\n'
}

TRANSLATION_MODEL_B = [
    model.Include('a', [model.Typedef('a', 'b')]),
    model.Constant('CONST_A', '0'),
]
TRANSLATION_WRITES_B = {
    'fake_out/mainer.em': '',
    'fake_out/mainer.st': """scope mainer {
<Include> [Include(name='a', nodes=[b a])]

<Constant> [Constant(name='CONST_A', value='0')]

} // endscope mainer
""",
}

TRANSLATION_MODEL_C = [
    model.Typedef('a', 'b'),
    model.Typedef('c', 'd'),
    model.Enum('E1', [
        model.EnumMember('E1_A', '0'),
        model.EnumMember('E1_B', '1')]),
    model.Enum('E2', [
        model.EnumMember('E2_A', '0')]),
    model.Constant('CONST_A', '0'),
    model.Constant('CONST_B', '0')
]

TRANSLATION_WRITES_C = {
    'fake_out/mainer.em': '',
    'fake_out/mainer.st': '''scope mainer {
<Typedef> [b a]
<Typedef> [d c]

<Enum> [E1
    E1_A 0
    E1_B 1
]

<Enum> [E2
    E2_A 0
]

<Constant> [Constant(name='CONST_A', value='0')]
<Constant> [Constant(name='CONST_B', value='0')]

} // endscope mainer
'''}


@pytest.mark.parametrize('nodes, writes', [
    (TRANSLATION_MODEL_A, TRANSLATION_WRITES_A),
    (TRANSLATION_MODEL_B, TRANSLATION_WRITES_B),
    (TRANSLATION_MODEL_C, TRANSLATION_WRITES_C)
])
def test_straigth_translation(serialize, nodes, writes):
    assert serialize(nodes) == writes


UNKNOWN_NONE_RAISE_TEST = [
    ([234], 'Unknown node type: int'),
    ([[12]], 'Unknown node type: list'),
    ([None], 'Unknown node type: NoneType')
]


@pytest.mark.parametrize('nodes, match', UNKNOWN_NONE_RAISE_TEST)
def test_raise_on_unknown_node(straigth_generator, nodes, match):
    gen = straigth_generator('.')
    with pytest.raises(GenerateError, match=match):
        gen.serialize(nodes, '')
