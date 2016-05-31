import os

import ply.lex as lex
import ply.yacc as yacc

from prophyc.six import ifilter
from prophyc.model import Include, Constant, Typedef, Enum, EnumMember, Struct, StructMember, Union, UnionMember, Kind, ParseError
from prophyc.file_processor import CyclicIncludeError, FileNotFoundError

def get_column(input, pos):
    return pos - input.rfind('\n', 0, pos)

class Parser(object):

    literals = ['+','-','*','/', '(',')','#']

    keywords = (
        "const", "enum", "typedef", "struct", "union",
        "u8", "u16", "u32", "u64", "i8", "i16", "i32", "i64",
        "float", "double", "bytes"
    )

    tokens = tuple([t.upper() for t in keywords]) + (
        "ID", "PATH", "CONST8", "CONST10", "CONST16",
        # [ ] { } < >
        "LBRACKET", "RBRACKET", "LBRACE", "RBRACE", "LT", "GT",
        # ; : = , ...
        "SEMI", "COLON", "EQUALS", "COMMA", "DOTS",
        # << >> @
        "LSHIFT", "RSHIFT", "AT"
    )

    def t_ID(self, t):
        r'[A-Za-z][A-Za-z0-9_]*'
        if t.value in self.keywords:
            t.type = t.value.upper()
        return t

    def t_PATH(self, t):
        r'".*"'
        return t

    def t_CONST16(self, t):
        r'0x[0-9a-fA-F]+'
        t.value = int(t.value, 16)
        return t

    def t_CONST8(self, t):
        r'0[0-7]+'
        t.value = int(t.value, 8)
        return t

    def t_CONST10(self, t):
        r'(([1-9]\d*)|0)'
        t.value = int(t.value)
        return t

    t_LBRACKET = r'\['
    t_RBRACKET = r'\]'
    t_LBRACE = r'\{'
    t_RBRACE = r'\}'
    t_SEMI = r';'
    t_COLON = r':'
    t_LT = r'<'
    t_GT = r'>'
    t_EQUALS = r'='
    t_COMMA = r','
    t_DOTS = r'\.\.\.'
    t_LSHIFT = r'<<'
    t_RSHIFT = r'>>'
    t_AT = r'@'

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
        self._parser_error("illegal character '{}'".format(t.value[0]), t.lexer.lineno, t.lexpos)

    precedence = (
        ('left', '+', '-'),
        ('left', '*', '/'),
        ('left', 'LSHIFT', 'RSHIFT'),
        ('right', 'UMINUS')
    )

    def __init__(self):
        self._init_parse_data()
        self.lexer = lex.lex(module = self, debug = 0)
        self.yacc = yacc.yacc(module = self, tabmodule = 'parsetab_prophy', write_tables = 0, debug = 0)

    def parse(self, input, parse_error_prefix, parse_file):
        self._init_parse_data(parse_error_prefix)
        self.parse_file = parse_file
        self.lexer.lineno = 1
        self.yacc.parse(input, lexer = self.lexer)
        return self.nodes

    def _init_parse_data(self, parse_error_prefix = ""):
        self.nodes = []
        self.typedecls = {}
        self.constdecls = {}
        self.errors = []
        self.parse_error_prefix = parse_error_prefix

    def _parser_error(self, message, line, pos):
        self.errors.append(("{}:{}:{}".format(
            self.parse_error_prefix,
            line,
            get_column(self.lexer.lexdata, pos)
        ), message))

    def _parser_check(self, condition, message, line, pos):
        if not condition:
            self._parser_error(message, line, pos)

    def _validate_struct_members(self, members):
        fieldnames = set()
        for i, (member, line, pos) in enumerate(members):
            name = member.name
            self._parser_check(
                name not in fieldnames,
                "field '{}' redefined".format(name),
                line, pos
            )
            fieldnames.add(name)
            if member.bound:
                bound, _, _ = next(ifilter(lambda m: m[0].name == member.bound, members[:i]),
                                   (None, None, None))
                if bound:
                    self._parser_check(self._is_type_sizer_compatible(bound.type_),
                                       "Sizer of '{}' has to be of (unsigned) integer type".format(name),
                                       line, pos)
                else:
                    self._parser_error("Sizer of '{}' has to be defined before the array".format(name),
                                       line, pos)

        for member, line, pos in members[:-1]:
            self._parser_check(
                not member.greedy and member.kind != Kind.UNLIMITED,
                "greedy array field '{}' not last".format(member.name),
                line, pos
            )

    def _is_type_sizer_compatible(self, typename):
        if typename in {type_ + width for type_ in 'ui' for width in ['8', '16', '32', '64']}:
            return True
        elif typename in self.typedecls and isinstance(self.typedecls[typename], Typedef):
            return self._is_type_sizer_compatible(self.typedecls[typename].type_)
        else:
            return False

    def p_specification(self, t):
        '''specification : definition_list'''

    def p_definition_list(self, t):
        '''definition_list : definition definition_list
                           | empty'''

    def p_definition(self, t):
        '''definition : include_def
                      | constant_def
                      | enum_def
                      | typedef_def
                      | struct_def
                      | union_def'''

    def p_include_def(self, t):
        """include_def : '#' ID PATH"""
        self._parser_check(
            t[2] == 'include',
            "unknown directive '{}'".format(t[2]),
            t.lineno(2), t.lexpos(2)
        )
        path = t[3][1:-1]
        stem = os.path.splitext(os.path.basename(path))[0]

        try:
            nodes = self.parse_file(path)
        except (CyclicIncludeError, FileNotFoundError) as e:
            self._parser_error(str(e), t.lineno(3), t.lexpos(3))
            nodes = []

        for node in nodes:
            if isinstance(node, Constant):
                self.constdecls[node.name] = node
            if isinstance(node, Enum):
                for mem in node.members:
                    self.constdecls[mem.name] = mem
            if isinstance(node, (Typedef, Enum, Struct, Union)):
                self.typedecls[node.name] = node

        node = Include(stem, nodes)
        self.nodes.append(node)

    def p_constant_def(self, t):
        '''constant_def : CONST unique_id EQUALS expression SEMI'''
        node = Constant(t[2], str(t[4]))
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
        '''enum_member : unique_id EQUALS expression'''
        member = EnumMember(t[1], str(t[3]))
        self.constdecls[t[1]] = member
        t[0] = member

    def p_typedef_def(self, t):
        '''typedef_def : TYPEDEF type_spec unique_id SEMI'''
        node = Typedef(t[3], t[2][0], definition = t[2][1])
        self.typedecls[t[3]] = node
        self.nodes.append(node)

    def p_struct_def(self, t):
        '''struct_def : STRUCT unique_id struct_body SEMI'''

        self._validate_struct_members(t[3])

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
        '''struct_member : bytes ID LBRACKET positive_expression RBRACKET
                         | type_spec ID LBRACKET positive_expression RBRACKET'''
        t[0] = [(StructMember(t[2], t[1][0], size = str(t[4]), definition = t[1][1]), t.lineno(2), t.lexpos(2))]

    def p_struct_member_3(self, t):
        '''struct_member : bytes ID LT AT ID GT
                         | type_spec ID LT AT ID GT'''
        t[0] = [
            (StructMember(t[2], t[1][0], bound = t[5], definition = t[1][1]), t.lineno(2), t.lexpos(2))
        ]

    def p_struct_member_4(self, t):
        '''struct_member : bytes ID LT GT
                         | type_spec ID LT GT'''
        t[0] = [
            (StructMember('num_of_' + t[2], 'u32', definition = None), t.lineno(2), t.lexpos(2)),
            (StructMember(t[2], t[1][0], bound = 'num_of_' + t[2], definition = t[1][1]), t.lineno(2), t.lexpos(2))
        ]

    def p_struct_member_5(self, t):
        '''struct_member : bytes ID LT positive_expression GT
                         | type_spec ID LT positive_expression GT'''
        t[0] = [
            (StructMember('num_of_' + t[2], 'u32', definition = None), t.lineno(2), t.lexpos(2)),
            (StructMember(t[2], t[1][0], bound = 'num_of_' + t[2], size = str(t[4]), definition = t[1][1]), t.lineno(2), t.lexpos(2))
        ]

    def p_struct_member_6(self, t):
        '''struct_member : bytes ID LT DOTS GT
                         | type_spec ID LT DOTS GT'''
        t[0] = [(StructMember(t[2], t[1][0], unlimited = True, definition = t[1][1]), t.lineno(2), t.lexpos(2))]

    def p_struct_member_7(self, t):
        '''struct_member : type_spec '*' ID'''
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
        '''union_member : expression COLON type_spec ID'''
        t[0] = (UnionMember(t[4], t[3][0], str(t[1]), definition = t[3][1]), t.lineno(4), t.lexpos(4))

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

    def p_positive_expression(self, t):
        '''positive_expression : expression'''
        self._parser_check(
            t[1] > 0,
            "array size '{}' non-positive".format(t[1]),
            t.lineno(1), t.lexpos(1)
        )
        t[0] = t[1]

    def p_expression_binop(self, t):
        '''expression : expression '+' expression
                      | expression '-' expression
                      | expression '*' expression
                      | expression '/' expression
                      | expression LSHIFT expression
                      | expression RSHIFT expression'''
        try:
            if t[2] == '+'  : t[0] = t[1] + t[3]
            elif t[2] == '-': t[0] = t[1] - t[3]
            elif t[2] == '*': t[0] = t[1] * t[3]
            elif t[2] == '/': t[0] = t[1] / t[3]
            elif t[2] == '<<': t[0] = t[1] << t[3]
            elif t[2] == '>>': t[0] = t[1] >> t[3]
        except ZeroDivisionError:
            self._parser_error(
                'division by zero',
                t.lineno(1), t.lexpos(1)
            )
            t[0] = 0
        t.slice[0].lineno = t.lineno(1)
        t.slice[0].lexpos = t.lexpos(1)

    def p_expression_uminus(self, t):
        "expression : '-' expression %prec UMINUS"
        t[0] = -t[2]
        t.slice[0].lineno = t.lineno(1)
        t.slice[0].lexpos = t.lexpos(1)

    def p_expression_group(self, t):
        "expression : '(' expression ')'"
        t[0] = t[2]
        t.slice[0].lineno = t.lineno(1)
        t.slice[0].lexpos = t.lexpos(1)

    def p_expression_number(self, t):
        "expression : constant"
        t[0] = t[1]
        t.slice[0].lineno = t.lineno(1)
        t.slice[0].lexpos = t.lexpos(1)

    def p_expression_name(self, t):
        "expression : ID"
        const = self.constdecls.get(t[1])
        self._parser_check(
            const,
            "constant '{}' was not declared".format(t[1]),
            t.lineno(1), t.lexpos(1)
        )
        t[0] = const and int(const.value) or 0
        t.slice[0].lineno = t.lineno(1)
        t.slice[0].lexpos = t.lexpos(1)

    def p_constant(self, t):
        '''constant : CONST10
                    | CONST8
                    | CONST16'''
        t[0] = t[1]
        t.slice[0].lineno = t.lineno(1)
        t.slice[0].lexpos = t.lexpos(1)

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

"""
Creating parsers is very expensive, so there is a need to reuse them.
On the other hand, recursive parser usage requires a unique one for each
level of recursion. Static stack of parsers seems to solve the issue.
"""
from contextlib import contextmanager
@contextmanager
def allocate_parser(parsers = []):
    parser = parsers and parsers.pop() or Parser()
    try:
        yield parser
    finally:
        parsers.append(parser)

def build_model(input, parse_error_prefix, parse_file):
    with allocate_parser() as parser:
        parser.parse(input, parse_error_prefix, parse_file)
        if parser.errors:
            raise ParseError(parser.errors)
        return parser.nodes

class ProphyParser(object):

    def parse(self, content, path, parse_file):
        return build_model(content, path, parse_file)
