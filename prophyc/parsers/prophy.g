start : specification;

@specification : newline (definition newline)*;

@definition:
      constant_def
    | typedef_def
    | enum_def
    | struct_def
    | 'union\s' identifier newline union_body ';'
    ;

constant_def:
    'const\s' identifier '=' constant ';';

typedef_def:
    'typedef\s' type_specifier identifier ';';

enum_def:
    'enum\s' identifier newline enum_body ';';

struct_def:
    'struct\s' identifier newline struct_body ';';

enum_body:
    '{'
    newline
        enumerator_spec
        ( ',' newline enumerator_spec )*
    newline
    '}'
    ;

enumerator_spec:
    identifier '=' value;

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
    | bytes identifier '\[' value ']'
    | bytes identifier '<' value? '>'
    ;

@type_specifier :
      u8
    | u16
    | u32
    | u64
    | i8
    | i16
    | i32
    | i64
    | float
    | double
    | identifier
    ;

u8: 'u8\s';
u16: 'u16\s';
u32: 'u32\s';
u64: 'u64\s';
i8: 'i8\s';
i16: 'i16\s';
i32: 'i32\s';
i64: 'i64\s';
float: 'float\s';
double: 'double\s';
bytes: 'bytes\s';

@value:
    constant | identifier;

constant : decimal_constant | hexadecimal_constant | octal_constant;

@decimal_constant : '-?[1-9]\d*';

@hexadecimal_constant : '0x[\da-f]*';

@octal_constant : '0o?[0-7]*';

identifier: '\w+';

@newline: (NEWLINE | SLASH_COMMENT | ASTERISK_COMMENT | WHITESPACE)*;

WHITESPACE: '[\t \f]+' (%ignore);

NEWLINE: '(\r?\n[\t ]*)+' (%newline);

SLASH_COMMENT: '//[^\n]*' (%ignore);

ASTERISK_COMMENT: '/\*[\s\S]+?\*/' (%ignore);
