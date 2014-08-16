import os
import tempfile

import ply.lex as lex
import ply.yacc as yacc

from prophyc.model import Constant, Typedef, Enum, EnumMember, Struct, StructMember, Union, UnionMember, Kind

PROPHY_DIR = os.path.join(tempfile.gettempdir(), '.prophy')

if not os.path.exists(PROPHY_DIR):
    os.makedirs(PROPHY_DIR)

class ParseError(Exception):
    def __init__(self, errors):
        Exception.__init__(self, "parsing error")
        self.errors = errors

def get_column(input, pos):
    return pos - input.rfind('\n', 0, pos)

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

    def _lexer_error(self, message, line, pos):
        None

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
        self._lexer_error("illegal character '{}'".format(t.value[0]), t.lexer.lineno, t.lexpos)

class Parser(object):

    def __init__(self, tokens, lexer, **kwargs):
        self._init_parse_data()
        self.tokens = tokens
        self.lexer = lexer
        self.yacc = yacc.yacc(module = self, **kwargs)

    def parse(self, input, parse_error_prefix):
        self._init_parse_data(parse_error_prefix)
        self.lexer.lineno = 1
        self.yacc.parse(input)
        return self.nodes

    def _init_parse_data(self, parse_error_prefix = ""):
        self.nodes = []
        self.typedecls = {}
        self.constdecls = {}
        self.errors = []
        self.parse_error_prefix = parse_error_prefix

    def _parser_error(self, message, line, pos):
        self.errors.append("{}:{}:{} error: {}".format(
            self.parse_error_prefix,
            line,
            get_column(self.lexer.lexdata, pos),
            message
        ))

    def _parser_check(self, condition, message, line, pos):
        if not condition:
            self._parser_error(message, line, pos)

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
        '''enum_member : unique_id EQUALS value'''
        member = EnumMember(t[1], t[3])
        self.constdecls[t[1]] = member
        t[0] = member

    def p_typedef_def(self, t):
        '''typedef_def : TYPEDEF type_spec unique_id SEMI'''
        node = Typedef(t[3], t[2][0], definition = t[2][1])
        self.typedecls[t[3]] = node
        self.nodes.append(node)

    def p_struct_def(self, t):
        '''struct_def : STRUCT unique_id struct_body SEMI'''

        fieldnames = set()
        for member, line, pos in t[3]:
            self._parser_check(
                member.name not in fieldnames,
                "field '{}' redefined".format(member.name),
                line, pos
            )
            fieldnames.add(member.name)
        for member, line, pos in t[3][:-1]:
            self._parser_check(
                not member.greedy and member.kind != Kind.UNLIMITED,
                "greedy array field '{}' not last".format(member.name),
                line, pos
            )

        node = Struct(t[2], [x for x, _, _ in t[3]])
        self.typedecls[t[2]] = node
        self.nodes.append(node)

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
        t[0] = [(StructMember(t[2], t[1][0], definition = t[1][1]), t.lineno(2), t.lexpos(2))]

    def p_struct_member_2(self, t):
        '''struct_member : bytes ID LBRACKET positive_value RBRACKET
                         | type_spec ID LBRACKET positive_value RBRACKET'''
        t[0] = [(StructMember(t[2], t[1][0], size = t[4], definition = t[1][1]), t.lineno(2), t.lexpos(2))]

    def p_struct_member_3(self, t):
        '''struct_member : bytes ID LT GT
                         | type_spec ID LT GT'''
        t[0] = [
            (StructMember('num_of_' + t[2], 'u32', definition = None), t.lineno(2), t.lexpos(2)),
            (StructMember(t[2], t[1][0], bound = 'num_of_' + t[2], definition = t[1][1]), t.lineno(2), t.lexpos(2))
        ]

    def p_struct_member_4(self, t):
        '''struct_member : bytes ID LT positive_value GT
                         | type_spec ID LT positive_value GT'''
        t[0] = [
            (StructMember('num_of_' + t[2], 'u32', definition = None), t.lineno(2), t.lexpos(2)),
            (StructMember(t[2], t[1][0], bound = 'num_of_' + t[2], size = t[4], definition = t[1][1]), t.lineno(2), t.lexpos(2))
        ]

    def p_struct_member_5(self, t):
        '''struct_member : bytes ID LT DOTS GT
                         | type_spec ID LT DOTS GT'''
        t[0] = [(StructMember(t[2], t[1][0], unlimited = True, definition = t[1][1]), t.lineno(2), t.lexpos(2))]

    def p_struct_member_6(self, t):
        '''struct_member : type_spec STAR ID'''
        t[0] = [(StructMember(t[3], t[1][0], optional = True, definition = t[1][1]), t.lineno(3), t.lexpos(3))]

    def p_bytes(self, t):
        '''bytes : BYTES'''
        t[0] = ('byte', None)

    def p_union_def(self, t):
        '''union_def : UNION unique_id union_body SEMI'''

        fieldnames = set()
        for member, line, pos in t[3]:
            self._parser_check(
                member.name not in fieldnames,
                "field '{}' redefined".format(member.name),
                line, pos
            )
            fieldnames.add(member.name)
        discriminatorvalues = set()
        for member, line, pos in t[3]:
            self._parser_check(
                member.discriminator not in discriminatorvalues,
                "duplicate discriminator value '{}'".format(member.discriminator),
                line, pos
            )
            discriminatorvalues.add(member.discriminator)
        for member, line, pos in t[3]:
            self._parser_check(
                member.kind == Kind.FIXED,
                "dynamic union arm '{}'".format(member.name),
                line, pos
            )

        node = Union(t[2], [x for x, _, _ in t[3]])
        self.typedecls[t[2]] = node
        self.nodes.append(node)

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
        t[0] = (UnionMember(t[4], t[3][0], t[1], definition = t[3][1]), t.lineno(4), t.lexpos(4))

    def p_type_spec_1(self, t):
        '''type_spec : U8
                     | U16
                     | U32
                     | U64
                     | I8
                     | I16
                     | I32
                     | I64'''
        t[0] = (t[1], None)

    def p_type_spec_2(self, t):
        '''type_spec : FLOAT'''
        t[0] = ('r32', None)

    def p_type_spec_3(self, t):
        '''type_spec : DOUBLE'''
        t[0] = ('r64', None)

    def p_type_spec_4(self, t):
        '''type_spec : ID'''
        self._parser_check(
            t[1] in self.typedecls,
            "type '{}' was not declared".format(t[1]),
            t.lineno(1), t.lexpos(1)
        )
        t[0] = (t[1], self.typedecls.get(t[1]))

    def p_unique_id(self, t):
        '''unique_id : ID'''
        self._parser_check(
            t[1] not in self.typedecls and t[1] not in self.constdecls,
            "name '{}' redefined".format(t[1]),
            t.lineno(1), t.lexpos(1)
        )
        t[0] = t[1]

    def p_constant_id(self, t):
        '''constant_id : ID'''
        self._parser_check(
            t[1] in self.constdecls,
            "constant '{}' was not declared".format(t[1]),
            t.lineno(1), t.lexpos(1)
        )
        t[0] = t[1]

    def p_positive_constant(self, t):
        '''positive_constant : CONST10
                             | CONST8
                             | CONST16'''
        self._parser_check(
            int(t[1]) > 0,
            "array size '{}' non-positive".format(t[1]),
            t.lineno(1), t.lexpos(1)
        )
        t[0] = t[1]

    def p_constant(self, t):
        '''constant : CONST10
                    | CONST8
                    | CONST16'''
        t[0] = t[1]

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
            message = "syntax error at '{}'".format(t.value)
            line = t.lexer.lineno
            pos = t.lexpos
        else:
            message = "unexpected end of input"
            line = self.lexer.lineno
            pos = len(self.lexer.lexdata) - 1
        self._parser_error(message, line, pos)

lexer = Lexer()
parser = Parser(lexer.tokens, lexer.lexer, debug = 0, outputdir = PROPHY_DIR)
lexer._lexer_error = parser._parser_error

def build_model(input, parse_error_prefix):
    parser.parse(input, parse_error_prefix)
    if parser.errors:
        raise ParseError(parser.errors)
    return parser.nodes

class ProphyParser(object):

    def parse_string(self, input):
        return build_model(input, "")

    def parse(self, filename):
        return build_model(open(filename).read(), os.path.split(filename)[1])
