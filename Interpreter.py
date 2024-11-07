from Parser import *
from Structures import *
from Predicate import *

class Interpreter:
    def __init__(self):
        self.state = {}

    #Statement Execution
    def initializeVar(self, Id, value):
        if(Id in self.state):
            self.state[Id].setValue(value)
            
        self.state[Id] = value
        #print(f"Initializing variable {Id}, with {value}")

    def execute_operation(self, operator, objct, op_args):
        getattr(objct, operator)(op_args, False)

    def execute_operation_as_expression(self, operator, objct, op_args):
        op = getattr(objct, operator)
        val = op(op_args, True)
        return val

    def execute_loop(self, IDs, objct, statement):
        for vals in objct.Iterate():
            
            for i, id in enumerate(IDs):
                self.state[id] = vals[i]
            #print(self.state)
            self.interpret(statement)

        for i, id in enumerate(IDs):
                self.state[id] = vals[i]

    #Tree traversal 
    def interpret(self, node):

        if(type(node) == TerminalNode):
            #If the terminal node is an identifier, return the value attached to it 
            #in the program's state
            if(node.kind == TT_IDENTIFIER and node.value in self.state):
                return self.state[node.value]
            
            elif(node.kind == TT_IDENTIFIER and node.value not in self.state):
                return [node.value]
            
            elif(node.kind == TT_STRING_LITERAL):
                return Text(node.value)
            
            elif(node.kind == TT_NUMBER_LITERAL):
                return Number(node.value)
            
            return node.value 

        match node.symbol:
            case SymbolType.PROGRAM:
                self.interpret(node.children[0])

            case SymbolType.STATEMENTS:
                for child in node.children:
                    self.interpret(child)

            case SymbolType.MORE_STATEMENTS:
                self.interpret(node.children[0])

            case SymbolType.STATEMENT:
                self.interpret(node.children[0])

            case SymbolType.LOOP:
                IDs = self.interpret(node.children[0])
                objct = self.interpret(node.children[1])
                statement = node.children[2]

                self.execute_loop(IDs, objct, statement)

            case SymbolType.VAR_INIT:
                Id = node.children[0].value
                value = self.interpret(node.children[1])

                self.initializeVar(Id, value)

            case SymbolType.OPERATION:
                operator = self.interpret(node.children[0])
                objct = self.interpret(node.children[1])

                objct_member = self.interpret(node.children[2])
                op_predicate = self.interpret(node.children[3])
                args = self.interpret(node.children[4])

                op_args = [objct_member, op_predicate, args]

                self.execute_operation(operator, objct, op_args)


            case SymbolType.IDENTIFIERS:
                IDs = []
                for child in node.children:
                    next_id = self.interpret(child)
                    if(next_id):
                        IDs += next_id
                return IDs
            
            case SymbolType.MORE_IDENTIFIERS:
                return self.interpret(node.children[0])

            case SymbolType.EXPRESSION:
                value = self.interpret(node.children[0])
                return value 
            
            case SymbolType.EXPRESSION_OPERATION:
                operator = self.interpret(node.children[0])
                objct = self.interpret(node.children[1])

                objct_member = self.interpret(node.children[2])
                op_predicate = self.interpret(node.children[3])
                args = self.interpret(node.children[4])

                op_args = [objct_member, op_predicate, args]

                value = self.execute_operation_as_expression(operator, objct, op_args)
                return value


            case SymbolType.OBJECT:
                return self.interpret(node.children[0])
            
            case SymbolType.OBJECT_INIT:
                if(len(node.children) == 1):
                    return self.interpret(node.children[0])
                
                objType = self.interpret(node.children[0])
                args = self.interpret(node.children[1])

                return structures[objType](args)

            case SymbolType.OBJECT_MEMBER:
                data_type = self.interpret(node.children[0])
                plural_modifier = None
                if(len(node.children) == 2):
                    plural_modifier = self.interpret(node.children[1])

                return [data_type, plural_modifier]

            case SymbolType.PLURAL_MODIFIER:
                return self.interpret(node.children[0])
        

            case SymbolType.PREDICATE:
                if(type(node.children[0]) == TerminalNode and node.children[0].kind == "IDENTIFIER"):
                    if(node.children[0].value in self.state):
                        return self.state[node.children[0].value]
                    else:
                        raise Exception(f"{node.children[0].value} is not recognized")

                else:
                    return self.interpret(node.children[0])

            case SymbolType.PREDICATE_INIT:
                pred_type = self.interpret(node.children[0])
                args = self.interpret(node.children[1])

                return predicates[pred_type](args)

            case SymbolType.OPTIONAL_ARGS:
                return self.interpret(node.children[0])

            case SymbolType.ARGS:
                args = []
                for child in node.children:
                    nextArgs = self.interpret(child)
                    if(nextArgs):
                        args += nextArgs
                return args

            case SymbolType.MORE_ARGS:
                return self.interpret(node.children[0])

            case SymbolType.ARG:
                if(type(node.children[0]) == TerminalNode and node.children[0].kind == "IDENTIFIER"):
                    if(node.children[0].value in self.state):
                        return [self.state[node.children[0].value]]
                    else:
                        raise Exception(f"{node.children[0].value} is not recognized")

                else:
                    return [self.interpret(node.children[0])]
                
            case _:
                raise Exception(f"Unrecognized symmbol: {node.symbol}")