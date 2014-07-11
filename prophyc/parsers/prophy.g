start : specification;

@specification : newline definition*;

@definition:
    (type_def | constant_def) newline;

type_def:
      'typedef\s' type_specifier identifier ';'
    | 'enum\s' identifier newline enum_body ';'
    | 'struct\s' identifier newline struct_body ';'
    | 'union\s' identifier newline union_body ';'
    ;

constant_def:
    'const\s' identifier '=' constant ';';

enum_body:
    '{'
    newline
        ( identifier '=' value )
        ( ',' newline identifier '=' value )*
    newline
    '}'
    ;

struct_body:
    '{'
    newline
        ( declaration ';' )
        ( newline declaration ';' )*
    newline
    '}'
    ;

union_body:
    '{'
    newline
        case_spec
        ( newline case_spec )*
    newline
    '}'
    ;

case_spec:
    value ':' declaration ';';

declaration:
      type_specifier identifier
    | type_specifier identifier '\[' value ']'
    | type_specifier identifier '<' value? '>'
    | type_specifier '\*' identifier
    | 'bytes\s' identifier '\[' value ']'
    | 'bytes\s' identifier '<' value? '>'
    ;

type_specifier :
      'u8'
    | 'u16'
    | 'u32'
    | 'u64'
    | 'i8'
    | 'i16'
    | 'i32'
    | 'i64'
    | 'float\s'
    | 'double\s'
    | identifier
    ;

value:
    constant | identifier;

constant : decimal_constant | hexadecimal_constant | octal_constant;

decimal_constant : '[1-9]\d*';

hexadecimal_constant : '0x[\da-f]*';

octal_constant : '0o?[0-7]*';

identifier: '\w+';

@newline: (NEWLINE | SLASH_COMMENT | ASTERISK_COMMENT | WHITESPACE)*;

WHITESPACE: '[\t \f]+' (%ignore);

NEWLINE: '(\r?\n[\t ]*)+' (%newline);

SLASH_COMMENT: '//[^\n]*' (%ignore);

ASTERISK_COMMENT: '/\*[\s\S]+?\*/' (%ignore);
