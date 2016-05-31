import ply.lex as lex
import ply.yacc as yacc

class ParseError(Exception): pass

class Parser(object):
    """
    Base class for a lexer/parser that has the rules defined as methods
    """
    tokens = ()
    precedence = ()

    def __init__(self):
        self.lexer = lex.lex(module = self, debug = 0)
        self.parser = yacc.yacc(module = self, tabmodule = 'parsetab_calc', write_tables = 0, debug = 0)

    def eval(self, expr):
        return self.parser.parse(expr, lexer = self.lexer)

class Calc(Parser):

    tokens = ('NAME','NUMBER','LSHIFT','RSHIFT')

    literals = ['+','-','*','/', '(',')']

    t_NAME    = r'[a-zA-Z_][a-zA-Z0-9_]*'
    t_LSHIFT  = r'<<'
    t_RSHIFT  = r'>>'

    def t_NUMBER(self, t):
        r'\d+'
        t.value = int(t.value)
        return t

    t_ignore = " \t"

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += t.value.count("\n")

    def t_error(self, t):
        raise ParseError('illegal character %s' % t.value[0])

    precedence = (
        ('left', '+', '-'),
        ('left', '*', '/'),
        ('left', 'LSHIFT', 'RSHIFT'),
        ('right', 'UMINUS'),
    )

    def p_statement_expr(self, p):
        'statement : expression'
        p[0] = p[1]

    def p_expression_binop(self, p):
        '''expression : expression '+' expression
                      | expression '-' expression
                      | expression '*' expression
                      | expression '/' expression
                      | expression LSHIFT expression
                      | expression RSHIFT expression'''
        if p[2] == '+'  : p[0] = p[1] + p[3]
        elif p[2] == '-': p[0] = p[1] - p[3]
        elif p[2] == '*': p[0] = p[1] * p[3]
        elif p[2] == '/': p[0] = p[1] / p[3]
        elif p[2] == '<<': p[0] = p[1] << p[3]
        elif p[2] == '>>': p[0] = p[1] >> p[3]

    def p_expression_uminus(self, p):
        "expression : '-' expression %prec UMINUS"
        p[0] = -p[2]

    def p_expression_group(self, p):
        "expression : '(' expression ')'"
        p[0] = p[2]

    def p_expression_number(self, p):
        "expression : NUMBER"
        p[0] = p[1]

    def p_expression_name(self, p):
        "expression : NAME"
        try:
            p[0] = p[1]
            while not isinstance(p[0], int):
                p[0] = self.vars[p[0]]
        except LookupError:
            raise ParseError("numeric constant '%s' not found" % p[1])

    def p_error(self, p):
        raise ParseError("syntax error at '%s'" % p.value)

    def eval(self, expr, vars):
        self.vars = vars
        return super(Calc, self).eval(expr)

calc = Calc()

def eval(expr, vars):
    return calc.eval(expr, vars)
