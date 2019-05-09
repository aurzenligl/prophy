import ply.lex as lex
import ply.yacc as yacc


class ParseError(Exception):
    pass


class Calc(object):
    tokens = ('NAME', 'CONST16', 'CONST10', 'LSHIFT', 'RSHIFT')
    precedence = (
        ('left', '+', '-'),
        ('left', '*', '/'),
        ('left', 'LSHIFT', 'RSHIFT'),
        ('right', 'UMINUS'),
    )

    literals = ['+', '-', '*', '/', '(', ')', '|']

    t_NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'
    t_LSHIFT = r'<<'
    t_RSHIFT = r'>>'

    def __init__(self):
        self.lexer = lex.lex(module=self, debug=0)
        self.parser = yacc.yacc(module=self, tabmodule='parsetab_calc', write_tables=0, debug=0)
        self.vars = {}

    def eval(self, expr, vars_):
        self.vars = vars_
        return self.parser.parse(expr, lexer=self.lexer)

    @staticmethod
    def t_CONST16(t):
        r"""0x[0-9a-fA-F]+"""
        t.value = int(t.value, 16)
        return t

    @staticmethod
    def t_CONST10(t):
        r"""\d+"""
        t.value = int(t.value)
        return t

    t_ignore = " \t"

    @staticmethod
    def t_newline(t):
        r"""\n+"""
        t.lexer.lineno += t.value.count("\n")

    @staticmethod
    def t_error(t):
        raise ParseError('illegal character %s' % t.value[0])

    @staticmethod
    def p_statement_expr(p):
        """statement : expression"""
        p[0] = p[1]

    @staticmethod
    def p_expression_binop(p):
        """expression : expression '+' expression
                      | expression '-' expression
                      | expression '*' expression
                      | expression '/' expression
                      | expression '|' expression
                      | expression LSHIFT expression
                      | expression RSHIFT expression"""
        if p[2] == '+':
            p[0] = p[1] + p[3]
        elif p[2] == '-':
            p[0] = p[1] - p[3]
        elif p[2] == '*':
            p[0] = p[1] * p[3]
        elif p[2] == '/':
            p[0] = p[1] / p[3]
        elif p[2] == '<<':
            p[0] = p[1] << p[3]
        elif p[2] == '>>':
            p[0] = p[1] >> p[3]
        elif p[2] == '|':
            p[0] = p[1] | p[3]

    @staticmethod
    def p_expression_uminus(p):
        """expression : '-' expression %prec UMINUS"""
        p[0] = -p[2]

    @staticmethod
    def p_expression_group(p):
        """expression : '(' expression ')'"""
        p[0] = p[2]

    @staticmethod
    def p_expression_number(p):
        """expression : CONST10
                      | CONST16"""
        p[0] = p[1]

    def p_expression_name(self, p):
        """expression : NAME"""
        try:
            p[0] = p[1]
            while not isinstance(p[0], int):
                p[0] = self.vars[p[0]]
        except LookupError:
            raise ParseError("numeric constant '%s' not found" % p[1])

    def p_error(self, p):
        raise ParseError("syntax error at '%s'" % p.value)


calc = Calc()


def eval(expr, vars_):
    return calc.eval(expr, vars_)
