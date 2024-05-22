import sys

import click

from antlr4 import FileStream, CommonTokenStream, ParseTreeWalker

from Cobol85Lexer import Cobol85Lexer
from DataDivisionCobol85Listener import DataDivisionCobol85Listener
from Cobol85Parser import Cobol85Parser


def extract_structures(copybook_file):
    lexer = Cobol85Lexer(FileStream(copybook_file))
    tokens = CommonTokenStream(lexer)
    parser = Cobol85Parser(tokens)
    tree = parser.compilationUnit()

    extractor = DataDivisionCobol85Listener()
    walker = ParseTreeWalker()
    walker.walk(extractor, tree)
    return extractor.get_symbol_table()

@click.command()
@click.option("--copybook-file", type=str)
@click.option("--data-file", type=str)
@click.option("--section-name", type=str)
def cobol_data_parser(copybook_file, data_file, section_name):

    symbol_table = extract_structures(copybook_file)
    print(symbol_table)


if __name__ == '__main__':
    cobol_data_parser()
