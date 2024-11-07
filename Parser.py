from Lexer import *

class SymbolType:
    PROGRAM = 'PROGRAM'
    STATEMENTS = 'STATEMENTS'
    MORE_STATEMENTS = 'MORE_STATEMENTS'
    STATEMENT = 'STATEMENT'

    LOOP = "LOOP"
    VAR_INIT = 'VAR_INIT'
    OPERATION = 'OPERATION'

    EXPRESSION = 'EXPRESSION'
    EXPRESSION_OPERATION = 'EXPRESSION_OPERATION'

    OBJECT = 'OBJECT'
    OBJECT_INIT = 'OBJECT_INIT'
    OBJECT_MEMBER = 'OBJECT_MEMBER'
    PLURAL_MODIFIER = 'PLURAL_MODIFIER'

    PREDICATE = 'PREDICATE'
    PREDICATE_INIT = 'PREDICATE_INIT'

    IDENTIFIERS = 'IDENTIFIERS'
    MORE_IDENTIFIERS = 'MORE_IDENTIFIERS'

    OPTIONAL_ARGS = 'OPTIONAL_ARGS'
    ARGS = 'ARGUMENTS'
    MORE_ARGS = 'MORE_ARGS'
    ARG = 'ARGUMENT'

class NonTerminalNode:
    def __init__(self, symbol, children):
        self.symbol = symbol
        self.children = children

    def __str__(self):
        s = f"[{self.symbol}: "
        if(type(self.children) == list):
            for child in self.children:
                s += str(child)
        else:
            s += str(self.children)
        s += ']'

        return s

class TerminalNode:
    def __init__(self, kind, value):
        self.kind = kind
        self.value = value

    def __str__(self):
        return '{' + f'{self.kind}:{self.value}' + '}'
    
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.index = 0
        self.current_token = self.tokens[self.index]

    def advance(self):
        self.index += 1
        self.current_token = self.tokens[self.index]

    def parse(self):
        parse_tree = self.program()
        return parse_tree


    #------------------STRUCTURE------------------------
    def program(self) -> NonTerminalNode:
        statements = self.statements()
        if(self.current_token.kind == TT_EOF):
            return NonTerminalNode(SymbolType.PROGRAM, [statements])
        else:
            raise Exception("Unexpected token" + self.current_token)
    
    def statements(self) -> NonTerminalNode:
        statement = self.statement()
        more_statements = self.more_statements()
        return NonTerminalNode(SymbolType.STATEMENTS, [statement, more_statements])

    def more_statements(self) -> NonTerminalNode:
        if(self.current_token.kind == TT_NEWLINE):
            self.advance() #match \n
            statements = self.statements()
            return NonTerminalNode(SymbolType.MORE_STATEMENTS, [statements])
        
        elif(self.current_token.kind == TT_EOF):
            terminal = TerminalNode(TT_NONE, None)
            return NonTerminalNode(SymbolType.MORE_STATEMENTS, [terminal])
        
        elif(self.current_token.kind == TT_R_BRACKET):
            terminal = TerminalNode(TT_NONE, None)
            return NonTerminalNode(SymbolType.MORE_STATEMENTS, [terminal])
        
        else:
            raise Exception("Unexpected token: " + self.current_token.value)

    def statement(self) -> NonTerminalNode:

        if(self.current_token.kind == TT_LOOP):
            loop = self.loop()
            return NonTerminalNode(SymbolType.STATEMENT, [loop])
        
        elif(self.current_token.kind == TT_IDENTIFIER):
            varInit = self.variable_init()
            return NonTerminalNode(SymbolType.STATEMENT, [varInit])

        elif(self.current_token.kind == TT_OPERATOR):
            operation = self.operation()
            return NonTerminalNode(SymbolType.STATEMENT, [operation])
        
        elif(self.current_token.kind == TT_NEWLINE or self.current_token.kind == TT_EOF):
            terminal = TerminalNode(TT_NONE, None)
            return NonTerminalNode(SymbolType.STATEMENT, [terminal])

        else:
            raise Exception("Unexpected token: " + self.current_token.value)


    #-----------------------------STATEMENT TYPES ------------------
    def loop(self) -> NonTerminalNode:
        if(self.current_token.kind == TT_LOOP):
            self.advance() #match ForAll token
        else:
            raise Exception("Expected a loop")
        
        if(self.current_token.kind == TT_IDENTIFIER):
            ID = self.identifiers()
            
        else:
            raise Exception("Expected an identifier")
        
        if(self.current_token.kind == TT_IN):
            self.advance() #match in token
        else:
            raise Exception("Expected a 'in'")
        
        objct = self.objct()

        if(self.current_token.kind == TT_COLON):
            self.advance() #match :
        else:
            raise Exception("Expected ':'")
        
        statement = self.statement()
        
        return NonTerminalNode(SymbolType.LOOP, [ID, objct, statement])

    def variable_init(self) -> NonTerminalNode:
        if(self.current_token.kind == TT_IDENTIFIER):
            idTk = self.current_token
            ID = TerminalNode(idTk.kind, idTk.value)
            self.advance() #match identifier
        else:
            raise Exception("Expected an identifier")

        if(self.current_token.kind == TT_ASSIGN):
            self.advance() #match =
        else:
            raise Exception("Expected '='")
        
        expression = self.expression()

        return NonTerminalNode(SymbolType.VAR_INIT, [ID, expression])
    
    def operation(self) -> NonTerminalNode:
        op_operator = None
        op_object = None
        op_member = None
        op_predicate = None
        op_args = None

        if(self.current_token.kind == TT_OPERATOR):
            tk = self.current_token
            op_operator = TerminalNode(tk.kind, tk.value)
            self.advance() # Match operator
        else:
            raise Exception("Expected an operator")

        op_object = self.objct()
        op_member = self.object_member()
        op_predicate = self.predicate()
        op_args = self.optional_args()

        return NonTerminalNode(SymbolType.OPERATION, [op_operator,op_object,op_member,op_predicate,op_args])
        
   #------------------------------EXPRESSION ------------------------------------     
    
    def expression(self) -> NonTerminalNode:
        if(self.current_token.kind == TT_OPERATOR):
            operation = self.expression_operation()
            return NonTerminalNode(SymbolType.EXPRESSION, [operation])
        
        elif(self.current_token.kind == TT_TYPE or self.current_token.kind == TT_IDENTIFIER
                or self.current_token.kind == TT_STRING_LITERAL or self.current_token.kind == TT_NUMBER_LITERAL):
            objInit = self.objct()
            return NonTerminalNode(SymbolType.EXPRESSION, [objInit])
        
        elif(self.current_token.kind == TT_PREDICATE_TYPE):
            pred_init = self.predicate_init()
            return NonTerminalNode(SymbolType.EXPRESSION, [pred_init])
        
        else:
            raise Exception("Expected an operation, predicate, or object initialization")
        
    def expression_operation(self) -> NonTerminalNode:
        op_operator = None
        op_object = None
        op_member = None
        op_predicate = None
        op_args = None

        if(self.current_token.kind == TT_OPERATOR):
            tk = self.current_token
            op_operator = TerminalNode(tk.kind, tk.value)
            self.advance() # Match operator
        else:
            raise Exception("Expected an operator")

        op_object = self.objct()
        op_member = self.object_member()
        op_predicate = self.predicate()
        op_args = self.optional_args()

        return NonTerminalNode(SymbolType.EXPRESSION_OPERATION, [op_operator,op_object,op_member,op_predicate,op_args])
        
    #------------------------------OBJECTS ------------------------------------  
    def identifiers(self) -> NonTerminalNode:
        ID = None
        more_IDs = None

        if(self.current_token.kind == TT_IDENTIFIER):
            idTk = self.current_token
            ID = TerminalNode(idTk.kind, idTk.value)
            self.advance()
        else:
            raise Exception("Expected an identifier")
        
        more_IDs = self.more_identifiers()

        return NonTerminalNode(SymbolType.IDENTIFIERS, [ID, more_IDs])
    
    def more_identifiers(self) -> NonTerminalNode:
        if(self.current_token.kind == TT_COMMA):
            self.advance() #match comma
            IDs = self.identifiers()
            return NonTerminalNode(SymbolType.MORE_IDENTIFIERS, [IDs])

        
        else:
            terminal = TerminalNode(TT_NONE, None)
            return NonTerminalNode(SymbolType.MORE_IDENTIFIERS, [terminal])
            

    def objct(self) -> NonTerminalNode:
        if(self.current_token.kind == TT_IDENTIFIER):
            tk = self.current_token
            ID = TerminalNode(tk.kind, tk.value)
            self.advance() #match identifier
            return NonTerminalNode(SymbolType.OBJECT,[ID])

        elif(self.current_token.kind == TT_TYPE or self.current_token.kind == TT_STRING_LITERAL 
                or self.current_token.kind == TT_NUMBER_LITERAL):
            obj = self.object_init()
            return NonTerminalNode(SymbolType.OBJECT, [obj])
        
        else:
            raise Exception("Expected identifier or object initialization")
    
    def object_init(self) -> NonTerminalNode:
        objType = None
        objArgs = None

        if(self.current_token.kind == TT_STRING_LITERAL or self.current_token.kind == TT_NUMBER_LITERAL):
            tk = self.current_token
            self.advance()
            terminal = TerminalNode(tk.kind, tk.value)
            return NonTerminalNode(SymbolType.OBJECT_INIT, [terminal])


        if(self.current_token.kind == TT_TYPE):
            tk = self.current_token
            objType = TerminalNode(tk.kind, tk.value)
            self.advance() #Match type
        else:
            raise Exception("Expected a data type")
        
        if(self.current_token.kind == TT_L_BRACKET):
            self.advance() # match ]
        else:
            raise Exception(f"Expected [, encountered {self.current_token}" )
        
        objArgs = self.args()

        if(self.current_token.kind == TT_R_BRACKET):
            self.advance() # match ]
        else:
            raise Exception("Expected ]")

        return NonTerminalNode(SymbolType.OBJECT_INIT, [objType, objArgs])
        
    def object_member(self) -> NonTerminalNode:
        if(self.current_token.kind == TT_TYPE):
            tk = self.current_token
            data_type = TerminalNode(tk.kind,tk.value)
            self.advance() # Match type
            plural_mod = self.plural_modifier()
            return NonTerminalNode(SymbolType.OBJECT_MEMBER, [data_type, plural_mod])
        
        elif(self.current_token.kind == TT_COLON or self.current_token.kind == TT_L_BRACKET
                or self.current_token.kind == TT_PREDICATE_TYPE or self.current_token.kind == TT_IDENTIFIER
                or self.current_token.kind == TT_NEWLINE or self.current_token.kind == TT_EOF):
            terminal = TerminalNode(TT_NONE, None)
            return NonTerminalNode(SymbolType.OBJECT_MEMBER, [terminal])

        else:
            raise Exception(f"Unexpected token " + self.current_token)
        
    def plural_modifier(self) -> NonTerminalNode:
        if(self.current_token.kind == TT_PLURAL):
            tk = self.current_token
            plural = TerminalNode(tk.kind, tk.value)
            self.advance() #match s
            return NonTerminalNode(SymbolType.PLURAL_MODIFIER, [plural])
        
        elif(self.current_token.kind == TT_COLON or self.current_token.kind == TT_L_BRACKET
                or self.current_token.kind == TT_PREDICATE_TYPE or self.current_token.kind == TT_IDENTIFIER
                or self.current_token.kind == TT_NEWLINE or self.current_token.kind == TT_EOF):
            terminal = TerminalNode(TT_NONE, None)
            return NonTerminalNode(SymbolType.PLURAL_MODIFIER, [terminal])
        
        else:
            raise Exception(f"Unexpected token {self.current_token}")

    def predicate(self) -> NonTerminalNode:
        if(self.current_token.kind == TT_IDENTIFIER):
            tk = self.current_token
            self.advance()
            ID = TerminalNode(tk.kind, tk.value)
            return NonTerminalNode(SymbolType.PREDICATE, [ID])
        
        elif(self.current_token.kind == TT_PREDICATE_TYPE):
            pred = self.predicate_init()
            return NonTerminalNode(SymbolType.PREDICATE, [pred])
        
        elif(self.current_token.kind == TT_L_BRACKET or self.current_token.kind == TT_NEWLINE or 
             self.current_token.kind == TT_EOF):
            terminal = TerminalNode(TT_NONE, None)
            return NonTerminalNode(SymbolType.PREDICATE, [terminal])
        
        else:
            raise Exception(f"Expeted a predicate, arguments, or statement end. Encountered {self.current_token}")
        
    def predicate_init(self) -> NonTerminalNode:
        pred_type = None
        pred_args = None

        if(self.current_token.kind == TT_PREDICATE_TYPE):
            tk = self.current_token
            pred_type = TerminalNode(tk.kind, tk.value)
            self.advance() #Match predicate type
        else:
            raise Exception('Expected predicate type')
        
        if(self.current_token.kind == TT_NEWLINE):
            terminal = TerminalNode(TT_NONE, None)
            return NonTerminalNode(SymbolType.OPTIONAL_ARGS, [terminal])
        
        if(self.current_token.kind == TT_L_BRACKET):
            self.advance() # match [
        else:
            raise Exception("Expected [")
        
        pred_args = self.args()

        if(self.current_token.kind == TT_R_BRACKET):
            self.advance() # match ]
        else:
            raise Exception("Expected ]")

        return NonTerminalNode(SymbolType.PREDICATE_INIT, [pred_type, pred_args])

    #Args ------------------------------------------------------------------
    def optional_args(self) -> NonTerminalNode:
        if(self.current_token.kind == TT_NEWLINE or self.current_token.kind == TT_EOF):
            terminal = TerminalNode(TT_NONE, None)
            return NonTerminalNode(SymbolType.OPTIONAL_ARGS, [terminal])
        
        if(self.current_token.kind == TT_L_BRACKET):
            self.advance() # match [
        else:
            raise Exception("Expected [")
        
        args = self.args()

        if(self.current_token.kind == TT_R_BRACKET):
            self.advance() # match ]
        else:
            raise Exception("Expected ]")
        
        return NonTerminalNode(SymbolType.OPTIONAL_ARGS, [args])
       
    def args(self) -> NonTerminalNode:
        arg = self.arg()
        more_args = self.more_args()
        
        return NonTerminalNode(SymbolType.ARGS,[arg,more_args])

    def more_args(self) -> NonTerminalNode:
        if(self.current_token.kind == TT_R_BRACKET):
            terminal = TerminalNode(TT_NONE, None)
            return NonTerminalNode(SymbolType.MORE_ARGS, [terminal])

        elif(self.current_token.kind == TT_COMMA):
            self.advance()      
            args = self.args()
            return NonTerminalNode(SymbolType.MORE_ARGS, [args])

        else:
            raise Exception(f"Unexpected token {self.current_token}")

    def arg(self) -> NonTerminalNode:
        if(self.current_token.kind == TT_STRING_LITERAL or self.current_token.kind == TT_NUMBER_LITERAL):
            tk = self.current_token
            literal_arg = TerminalNode(tk.kind, tk.value)
            self.advance() #Match string or number literal
            return NonTerminalNode(SymbolType.ARG,[literal_arg])
        
        elif(self.current_token.kind == TT_IDENTIFIER or self.current_token.kind == TT_TYPE):
            obj = self.objct()
            return NonTerminalNode(SymbolType.ARG,[obj])
        
        