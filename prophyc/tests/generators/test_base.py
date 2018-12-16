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
    class EmptyTranslator(base.TranslatorBase):
        pass

    class StraightTranslator(base.TranslatorBase):
        block_template = '''scope {base_name} {{\n{content}\n}} // endscope {base_name}\n'''

        def __init__(self):
            for model_type, translator_name in base.TranslatorBase._translation_methods_map.items():
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
    writes = {}

    def write_mock(file_path, file_content):
        writes.update({file_path: file_content})

    mocker.patch.object(base, '_write_file', side_effect=write_mock)
    mocker.patch.object(base.os.path, 'isdir', return_value=True)

    def process(nodes, base_name='mainer'):
        model.cross_reference(nodes)
        model.evaluate_stiffness_kinds(nodes)
        model.evaluate_sizes(nodes)
        gen = straigth_generator('fake_out')
        gen.check_nodes(nodes)
        gen.serialize(nodes, base_name)

        return writes

    return process


def test_translatin_empty_model(serialize):
    assert serialize([]) == {
        'fake_out/mainer.em': '',
        'fake_out/mainer.st': 'scope mainer {\n\n} // endscope mainer\n'
    }


def test_straigth_translation_b(serialize):
    expecting_result = {
        'fake_out/mainer.em': '',
        'fake_out/mainer.st': """\
scope mainer {
<Include> [include a {
    typedef b a;;
};
]

<Constant> [const CONST_A = '0';]

} // endscope mainer
""",
    }

    result = serialize([
        model.Include('a', [model.Typedef('a', 'b')]),
        model.Constant('CONST_A', '0'),
    ])
    assert set(result.keys()) == set(expecting_result.keys())
    assert len(result) == len(expecting_result)
    assert sorted(result.values()) == sorted(expecting_result.values())


def test_straigth_translation_c(serialize):
    input_model = [
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

    expected_result = {
        'fake_out/mainer.em': '',
        'fake_out/mainer.st': '''\
scope mainer {
<Typedef> [typedef b a;]
<Typedef> [typedef d c;]

<Enum> [enum E1 {
    E1_A = '0';
    E1_B = '1';
};
]

<Enum> [enum E2 {
    E2_A = '0';
};
]

<Constant> [const CONST_A = '0';]
<Constant> [const CONST_B = '0';]

} // endscope mainer
'''}

    result = serialize(input_model)
    assert result == expected_result


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
