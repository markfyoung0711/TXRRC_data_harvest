import sys

from antlr4 import *

from Cobol85Lexer import Cobol85Lexer
from Cobol85Listener import Cobol85Listener
from Cobol85Parser import Cobol85Parser


def main(program_file):
    lexer = Cobol85Lexer(FileStream(program_file))
    tokens = CommonTokenStream(lexer)
    parser = Cobol85Parser(tokens)
    tree = parser.compilationUnit()

    extractor = Cobol85Listener()
    walker = ParseTreeWalker()
    walker.walk(extractor, tree)

if __name__ == '__main__':
    main(sys.argv[1])
