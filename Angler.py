import sys
from Lexer import tokenize
from Parser import Parser
from Interpreter import Interpreter


def main():
    if(len(sys.argv) == 1):
        localInterpreter = Interpreter()
        while True:
            statement = input("Angler $ ")
            try:
                tokens = tokenize(statement)
                localParser = Parser(tokens)
                syntax_tree = localParser.parse()

                localInterpreter.interpret(syntax_tree)

            except Exception as e:
                print(e)


    elif(len(sys.argv) == 2):
        file = sys.argv[1]
        with open(file, 'r') as file:
            program = file.read()

        tokens = tokenize(program)
        localParser = Parser(tokens)
        syntax_tree = localParser.parse()

        localInterpreter = Interpreter()
        localInterpreter.interpret(syntax_tree)


main()
