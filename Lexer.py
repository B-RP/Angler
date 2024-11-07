import re

TT_EOF = 'EOF'
TT_NEWLINE = 'NEWLINE'
TT_PLURAL = 's'
TT_L_BRACKET = 'L_BRACKET'
TT_R_BRACKET = 'R_BRACKET'
TT_COMMA = 'COMMA'
TT_ASSIGN = 'ASSIGN'
TT_COLON = 'COLON'
TT_OPERATOR = 'OPERATOR'
TT_LOOP = 'LOOP'
TT_IN = "IN"
TT_TYPE = 'TYPE'
TT_PREDICATE_TYPE = 'PREDICATE_TYPE'
TT_IDENTIFIER = 'IDENTIFIER'
TT_STRING_LITERAL = 'STRING_LITERAL'
TT_NUMBER_LITERAL = 'NUMBER_LITERAL'
TT_NONE = 'NONE'

operators = {'Filter', 'Remove', 'Count', 'Replace', 'Print', 'Read'}
types = {'File','Table', 'Record', 'Field', 'Value', 'Text', 'Line', 'Word', 'List','Number', 'Character'}
predicates = {'ByValue', 'ByMaxValue', 'ByMinValue', 'ByRange', "ByEndsWith", "ByValueAtCol", "ByMaxValueAtCol", "ByMinValueAtCol"}
class Token:
    def __init__(self, kind, value, line):
        self.kind = kind
        self.value = value
        self.line = line

    def __str__(self):
        return f"{'{'}'{self.kind}':'{self.value}'{'}'}"

    
token_specification = [
    (TT_NUMBER_LITERAL,  r'\d+(\.\d*)?'),  # Integer or decimal number
    (TT_STRING_LITERAL,  r'\"(.*?)\"'),    # String literal
    (TT_ASSIGN,          r'='),            # Assignment operator
    (TT_COMMA,           r','),            # Comma
    (TT_COLON,           r':'),            # Colon   
    (TT_L_BRACKET,       r'\['),           # Left parenthesis
    (TT_R_BRACKET,       r'\]'),           # Right parenthesis
    (TT_IDENTIFIER,      r'[A-Za-z]+'),    # Identifiers
    (TT_NEWLINE,         r'\n'),           # Line endings
    ('SKIP',             r'[ \t]+'),       # Skip over spaces and tabs
    ('MISMATCH',         r'.'),            # Any other character
]

errors = []

def tokenize(code):
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
    line_num = 1
    line_start = 0
    tokens = []
    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup
        value = mo.group()
        
        if kind == TT_NUMBER_LITERAL:
            value = float(value) if '.' in value else int(value)

        elif kind == TT_STRING_LITERAL:
            value = value.removeprefix('"')
            value = value.removesuffix('"')

        elif kind == TT_IDENTIFIER and value in operators:
            kind = TT_OPERATOR

        elif kind == TT_IDENTIFIER and value in types:
            kind = TT_TYPE

        elif kind == TT_IDENTIFIER and value in predicates:
            kind = TT_PREDICATE_TYPE

        elif kind == TT_IDENTIFIER and value == "ForAll":
            kind = TT_LOOP

        elif kind == TT_IDENTIFIER and value == "in":
            kind = TT_IN

        elif kind == TT_IDENTIFIER and value[-1] == 's':
            if(value[:-1] in types):
                tokens.append(Token(TT_TYPE, value[:-1], line_num))
                tokens.append(Token(TT_PLURAL, 's', line_num))
                continue
                
        elif kind == TT_NEWLINE:
            line_start = mo.end()
            line_num += 1
            value = 'NEWLINE'

        elif kind == 'SKIP':
            continue

        elif kind == 'MISMATCH':
            raise Exception(f"Illegal characater: {value}")

        tokens.append(Token(kind, value, line_num))
        
    tokens.append(Token(TT_EOF, 'EOF', line_num))
    return tokens
