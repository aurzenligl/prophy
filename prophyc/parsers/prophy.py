import os
import tempfile

import ply.lex as lex
import ply.yacc as yacc

from prophyc.model import Constant, Typedef, Enum, EnumMember, Struct, StructMember, Union, UnionMember

PROPHY_DIR = os.path.join(tempfile.gettempdir(), 'prophy')

if not os.path.exists(PROPHY_DIR):
    os.makedirs(PROPHY_DIR)

class ParseError(Exception): pass

class Lexer(object):

    keywords = (
        "const", "enum", "typedef", "struct", "union",
        "u8", "u16", "u32", "u64", "i8", "i16", "i32", "i64",
        "float", "double", "bytes"
    )

    tokens = tuple([t.upper() for t in keywords]) + (
        "ID", "CONST8", "CONST10", "CONST16",
        # [ ] { } < >
        "LBRACKET", "RBRACKET", "LBRACE", "RBRACE", "LT", "GT",
        # ; :  * = , ...
        "SEMI", "COLON", "STAR", "EQUALS", "COMMA", "DOTS"
    )

    def __init__(self, **kwargs):
        self.lexer = lex.lex(module = self, **kwargs)

    def t_ID(self, t):
        r'[A-Za-z][A-Za-z0-9_]*'
        if t.value in self.keywords:
            t.type = t.value.upper()
        return t

    def t_CONST16(self, t):
        r'0x[0-9a-fA-F]+'
        return t

    def t_CONST8(self, t):
        r'0[0-7]+'
        return t

    def t_CONST10(self, t):
        r'-?(([1-9]\d*)|0)'
        return t

    t_LBRACKET = r'\['
    t_RBRACKET = r'\]'
    t_LBRACE = r'\{'
    t_RBRACE = r'\}'
    t_SEMI = r';'
    t_COLON = r':'
    t_LT = r'<'
    t_GT = r'>'
    t_STAR = r'\*'
    t_EQUALS = r'='
    t_COMMA = r','
    t_DOTS = r'\.\.\.'

    t_ignore  = ' \t'

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    def t_comment(self, t):
        r'/\*(.|\n)*?\*/'
        t.lexer.lineno += t.value.count('\n')

    def t_linecomment(self, t):
        r'//.*\n'
        t.lexer.lineno += 1

    def t_error(self, t):
        print "Illegal character %s at %d type %s" % (repr(t.value[0]), t.lexer.lineno, t.type)
        t.lexer.skip(1)

class Parser(object):

    def __init__(self, tokens, lexer, **kwargs):
        self._clear_data()
        self.tokens = tokens
        self.lexer = lexer
        self.yacc = yacc.yacc(module = self, **kwargs)

    def parse(self, data):
        self._clear_data()
        self.yacc.parse(data)
        return self.nodes

    def _clear_data(self):
        self.nodes = []
        self.typedecls = {}
        self.constdecls = {}

    _builtin_types = ["u8", "u16", "u32", "u64", "i8", "i16", "i32", "i64", "r32", "r64", "byte"]
    _sanitizer_rules = {'float': 'r32', 'double': 'r64'}

    def _sanitize_type(self, name):
        return self._sanitizer_rules.get(name, name)

    def _validate_decl_not_defined(self, name):
        if name in self.typedecls or name in self.constdecls:
            raise ParseError("Name '{}' redefined".format(name))

    def _validate_typedecl_exists(self, type_):
        if type_ not in self._builtin_types and type_ not in self.typedecls:
            raise ParseError("Type '{}' was not declared".format(type_))

    def p_specification(self, t):
        '''specification : definition_list'''

    def p_definition_list(self, t):
        '''definition_list : definition definition_list
                           | empty'''

    def p_definition(self, t):
        '''definition : constant_def
                      | enum_def
                      | typedef_def
                      | struct_def
                      | union_def'''

    def p_constant_def(self, t):
        '''constant_def : CONST ID EQUALS constant SEMI'''
        name = t[2]
        value = t[4]
        self._validate_decl_not_defined(name)

        node = Constant(name, value)
        self.constdecls[name] = node
        self.nodes.append(node)

    def p_constant(self, t):
        '''constant : CONST10
                    | CONST8
                    | CONST16'''
        t[0] = t[1]

    def p_enum_def(self, t):
        '''enum_def : ENUM ID enum_body SEMI'''

    def p_enum_body(self, t):
        '''enum_body : LBRACE enum_member_list RBRACE'''

    def p_enum_member_list(self, t):
        '''enum_member_list : enum_member COMMA enum_member_list
                            | enum_member'''

    def p_enum_member(self, t):
        '''enum_member : ID EQUALS value'''

    def p_typedef_def(self, t):
        '''typedef_def : TYPEDEF type_spec ID SEMI'''
        type_ = self._sanitize_type(t[2])
        name = t[3]
        self._validate_decl_not_defined(name)
        self._validate_typedecl_exists(type_)

        node = Typedef(name, type_)
        self.typedecls[name] = node
        self.nodes.append(node)

    def p_struct_def(self, t):
        '''struct_def : STRUCT ID struct_body SEMI'''

    def p_struct_body(self, t):
        '''struct_body : LBRACE struct_member_list RBRACE'''

    def p_struct_member_list(self, t):
        '''struct_member_list : struct_member SEMI struct_member_list
                              | struct_member SEMI'''

    def p_struct_member(self, t):
        '''struct_member : BYTES ID optional_array_spec
                         | type_spec ID optional_array_spec
                         | type_spec STAR ID'''

    def p_optional_array_spec(self, t):
        '''optional_array_spec : array_spec
                               | empty'''

    def p_array_spec(self, t):
        '''array_spec : LBRACKET value RBRACKET
                      | LT value GT
                      | LT DOTS GT
                      | LT GT'''

    def p_union_def(self, t):
        '''union_def : UNION ID union_body SEMI'''

    def p_union_body(self, t):
        '''union_body : LBRACE union_member_list RBRACE'''

    def p_union_member_list(self, t):
        '''union_member_list : union_member SEMI union_member_list
                             | union_member SEMI'''

    def p_union_member(self, t):
        '''union_member : value COLON type_spec ID'''

    def p_type_spec(self, t):
        '''type_spec : U8
                     | U16
                     | U32
                     | U64
                     | I8
                     | I16
                     | I32
                     | I64
                     | FLOAT
                     | DOUBLE
                     | ID'''
        t[0] = t[1]

    def p_value(self, t):
        '''value : constant
                 | ID'''

    def p_empty(self, t):
        '''empty :'''

    def p_error(self, t):
        print "Syntax error in input!", "'{}'".format(t.value), 'line', t.lineno

def _is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def validate_constdecl_exists(state, value):
    if not _is_int(value) and value not in state.constdecls:
        raise Exception("Constant '{}' was not declared".format(value))

def validate_value_positive(state, value):
    if _is_int(value) and int(value) <= 0:
        raise Exception("Array size '{}' must be positive".format(value))

def validate_field_name_not_defined(names, name):
    if name in names:
        raise Exception("Field '{}' redefined".format(name))

def validate_value_not_defined(values, value):
    if value in values:
        raise Exception("Value '{}' redefined".format(value))

def validate_greedy_field_last(last_index, index, name):
    if index != last_index:
        raise Exception("Greedy array field '{}' not last".format(name))

def get_struct_type_specifier(tree):
    if tree.head == 'bytes':
        return 'byte'
    else:
        return get_type_specifier(tree)

def enum_def(state, tail):
    def enumerator_def(tree):
        name = str(tree.tail[0].tail[0])
        value = str(tree.tail[1].tail[0])
        validate_decl_not_defined(state, name)
        validate_constdecl_exists(state, value)

        member = EnumMember(name, value)
        state.constdecls[name] = member
        return member

    name = str(tail[0].tail[0])
    validate_decl_not_defined(state, name)

    node = Enum(name, [enumerator_def(tree) for tree in tail[1].tail])
    state.typedecls[name] = node
    return node

def struct_def(state, tail):
    def field_def(tail):
        names = set()
        last_index = len(tail) - 1
        for index, tree in enumerate(tail):
            type_ = get_struct_type_specifier(tree.tail[0])
            if tree.tail[1].head == 'optional':
                optional = True
                name = str(tree.tail[2].tail[0])
            else:
                optional = False
                name = str(tree.tail[1].tail[0])

            validate_field_name_not_defined(names, name)
            validate_typedecl_exists(state, type_)
            names.add(name)

            if len(tree.tail) > 2 and not optional:
                array = tree.tail[2]
                if array.head == 'fixed_array':
                    value = str(array.tail[0].tail[0])
                    validate_constdecl_exists(state, value)
                    validate_value_positive(state, value)
                    yield StructMember(name, type_, size = value)
                elif array.head == 'dynamic_array':
                    yield StructMember('num_of_' + name, 'u32')
                    yield StructMember(name, type_, bound = 'num_of_' + name)
                elif array.head == 'limited_array':
                    value = str(array.tail[0].tail[0])
                    validate_constdecl_exists(state, value)
                    validate_value_positive(state, value)
                    yield StructMember('num_of_' + name, 'u32')
                    yield StructMember(name, type_, bound = 'num_of_' + name, size = value)
                else:
                    validate_greedy_field_last(last_index, index, name)
                    yield StructMember(name, type_, unlimited = True)
            else:
                yield StructMember(name, type_, optional = optional)

    name = str(tail[0].tail[0])
    validate_decl_not_defined(state, name)

    node = Struct(name, [x for x in field_def(tail[1].tail)])
    state.typedecls[name] = node
    return node

def union_def(state, tail):
    def arm_def(tree, names = set(), values = set()):
        value = str(tree.tail[0].tail[0])
        type_ = get_type_specifier(tree.tail[1])
        name = str(tree.tail[2].tail[0])
        validate_typedecl_exists(state, type_)
        validate_constdecl_exists(state, value)
        validate_field_name_not_defined(names, name)
        validate_value_not_defined(values, value)
        values.add(value)
        names.add(name)
        return UnionMember(name, type_, value)

    name = str(tail[0].tail[0])
    validate_decl_not_defined(state, name)

    node = Union(name, [arm_def(x) for x in tail[1].tail])
    state.typedecls[name] = node
    return node

def build_model(string_):
    lexer = Lexer()
    parser = Parser(lexer.tokens, lexer.lexer, debug = 0, outputdir = PROPHY_DIR)
    return parser.parse(string_)

class ProphyParser(object):

    def parse_string(self, string_):
        return build_model(string_)

    def parse(self, filename):
        return build_model(open(filename).read())
