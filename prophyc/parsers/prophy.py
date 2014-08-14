import os
import tempfile

import ply.lex as lex
import ply.yacc as yacc

from prophyc.model import Constant, Typedef, Enum, EnumMember, Struct, StructMember, Union, UnionMember

PROPHY_DIR = os.path.join(tempfile.gettempdir(), 'prophy')

if not os.path.exists(PROPHY_DIR):
    os.makedirs(PROPHY_DIR)

class ParseError(Exception): pass

def get_column(input, pos):
    last_cr = input.rfind('\n', 0, pos)
    if last_cr < 0:
        last_cr = 0
    return (pos - last_cr) + 1

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

    t_ignore  = ' \t\r'

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
        t.lexer.skip(1)
        line = self.lexer.lineno
        col = get_column(self.lexer.lexdata, t.lexpos)
        raise ParseError(":{}:{} error: illegal character '{}'".format(line, col, t.value[0]))

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

    def _validate_typedecl_exists(self, type_):
        if type_ not in self.typedecls:
            raise ParseError("Type '{}' was not declared".format(type_))

    def _validate_constdecl_exists(self, value):
        if value not in self.constdecls:
            raise ParseError("Constant '{}' was not declared".format(value))

    def _validate_value_positive(self, value):
        if int(value) <= 0:
            raise ParseError("Array size '{}' must be positive".format(value))

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
        '''constant_def : CONST unique_id EQUALS constant SEMI'''
        node = Constant(t[2], t[4])
        self.constdecls[t[2]] = node
        self.nodes.append(node)

    def p_constant(self, t):
        '''constant : CONST10
                    | CONST8
                    | CONST16'''
        t[0] = t[1]

    def p_enum_def(self, t):
        '''enum_def : ENUM unique_id enum_body SEMI'''
        node = Enum(t[2], t[3])
        self.typedecls[t[2]] = node
        self.nodes.append(node)

    def p_enum_body(self, t):
        '''enum_body : LBRACE enum_member_list RBRACE'''
        t[0] = t[2]

    def p_enum_member_list_1(self, t):
        '''enum_member_list : enum_member COMMA enum_member_list'''
        t[0] = [t[1]] + t[3]

    def p_enum_member_list_2(self, t):
        '''enum_member_list : enum_member'''
        t[0] = [t[1]]

    def p_enum_member(self, t):
        '''enum_member : ID EQUALS value'''
        member = EnumMember(t[1], t[3])
        self.constdecls[t[1]] = member
        t[0] = member

    def p_typedef_def(self, t):
        '''typedef_def : TYPEDEF type_spec unique_id SEMI'''
        node = Typedef(t[3], t[2])
        self.typedecls[t[3]] = node
        self.nodes.append(node)

    def p_struct_def(self, t):
        '''struct_def : STRUCT unique_id struct_body SEMI'''
        node = Struct(t[2], t[3])
        self.typedecls[t[2]] = node
        self.nodes.append(node)
        # validate_field_name_not_defined(names, name)
        # validate_greedy_field_last(last_index, index, name)

    def p_struct_body(self, t):
        '''struct_body : LBRACE struct_member_list RBRACE'''
        t[0] = t[2]

    def p_struct_member_list_1(self, t):
        '''struct_member_list : struct_member SEMI struct_member_list'''
        t[0] = t[1] + t[3]

    def p_struct_member_list_2(self, t):
        '''struct_member_list : struct_member SEMI'''
        t[0] = t[1]

    def p_struct_member_1(self, t):
        '''struct_member : type_spec ID'''
        t[0] = [StructMember(t[2], t[1])]

    def p_struct_member_2(self, t):
        '''struct_member : bytes ID LBRACKET positive_value RBRACKET
                         | type_spec ID LBRACKET positive_value RBRACKET'''
        t[0] = [StructMember(t[2], t[1], size = t[4])]

    def p_struct_member_3(self, t):
        '''struct_member : bytes ID LT GT
                         | type_spec ID LT GT'''
        t[0] = [
            StructMember('num_of_' + t[2], 'u32'),
            StructMember(t[2], t[1], bound = 'num_of_' + t[2])
        ]

    def p_struct_member_4(self, t):
        '''struct_member : bytes ID LT positive_value GT
                         | type_spec ID LT positive_value GT'''
        t[0] = [
            StructMember('num_of_' + t[2], 'u32'),
            StructMember(t[2], t[1], bound = 'num_of_' + t[2], size = t[4])
        ]

    def p_struct_member_5(self, t):
        '''struct_member : bytes ID LT DOTS GT
                         | type_spec ID LT DOTS GT'''
        t[0] = [StructMember(t[2], t[1], unlimited = True)]

    def p_struct_member_6(self, t):
        '''struct_member : type_spec STAR ID'''
        t[0] = [StructMember(t[3], t[1], optional = True)]

    def p_bytes(self, t):
        '''bytes : BYTES'''
        t[0] = 'byte'

    def p_union_def(self, t):
        '''union_def : UNION unique_id union_body SEMI'''
        node = Union(t[2], t[3])
        self.typedecls[t[2]] = node
        self.nodes.append(node)
        #validate_field_name_not_defined(names, name)
        #validate_value_not_defined(values, value)

    def p_union_body(self, t):
        '''union_body : LBRACE union_member_list RBRACE'''
        t[0] = t[2]

    def p_union_member_list_1(self, t):
        '''union_member_list : union_member SEMI union_member_list'''
        t[0] = [t[1]] + t[3]

    def p_union_member_list_2(self, t):
        '''union_member_list : union_member SEMI'''
        t[0] = [t[1]]

    def p_union_member(self, t):
        '''union_member : value COLON type_spec ID'''
        t[0] = UnionMember(t[4], t[3], t[1])

    def p_type_spec_1(self, t):
        '''type_spec : U8
                     | U16
                     | U32
                     | U64
                     | I8
                     | I16
                     | I32
                     | I64'''
        t[0] = t[1]

    def p_type_spec_2(self, t):
        '''type_spec : FLOAT'''
        t[0] = 'r32'

    def p_type_spec_3(self, t):
        '''type_spec : DOUBLE'''
        t[0] = 'r64'

    def p_type_spec_4(self, t):
        '''type_spec : ID'''
        type_ = t[1]
        self._validate_typedecl_exists(type_)
        t[0] = type_

    def p_unique_id(self, t):
        '''unique_id : ID'''
        name = t[1]
        if name in self.typedecls or name in self.constdecls:
            raise ParseError(":{}:{} error: name '{}' redefined".format(
                t.lineno(1), get_column(self.lexer.lexdata, t.lexpos(1)), name))
        t[0] = name

    def p_constant_id(self, t):
        '''constant_id : ID'''
        const = t[1]
        self._validate_constdecl_exists(const)
        t[0] = const

    def p_positive_constant(self, t):
        '''positive_constant : constant'''
        const = t[1]
        self._validate_value_positive(const)
        t[0] = const

    def p_positive_value(self, t):
        '''positive_value : positive_constant
                          | constant_id'''
        t[0] = t[1]

    def p_value(self, t):
        '''value : constant
                 | constant_id'''
        t[0] = t[1]

    def p_empty(self, t):
        '''empty :'''

    def p_error(self, t):
        if t:
            line = self.lexer.lineno
            col = get_column(self.lexer.lexdata, t.lexpos)
            raise ParseError(":{}:{} error: syntax error at '{}'".format(line, col, t.value))
        else:
            line = self.lexer.lineno
            col = get_column(self.lexer.lexdata, len(self.lexer.lexdata) - 1)
            raise ParseError(":{}:{} error: unexpected end of input".format(line, col))

def validate_field_name_not_defined(names, name):
    if name in names:
        raise Exception("Field '{}' redefined".format(name))

def validate_value_not_defined(values, value):
    if value in values:
        raise Exception("Value '{}' redefined".format(value))

def validate_greedy_field_last(last_index, index, name):
    if index != last_index:
        raise Exception("Greedy array field '{}' not last".format(name))

def build_model(string_):
    lexer = Lexer()
    parser = Parser(lexer.tokens, lexer.lexer, debug = 0, outputdir = PROPHY_DIR)
    return parser.parse(string_)

class ProphyParser(object):

    def parse_string(self, string_):
        return build_model(string_)

    def parse(self, filename):
        return build_model(open(filename).read())
