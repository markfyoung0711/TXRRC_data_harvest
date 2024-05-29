import re
import struct
import sys

import click
import yaml

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

def get_dataset_config(record_type_config_file):

    with open(record_type_config_file, 'r') as input_file:

        # Parsing
        # 1. open record type config yaml
        return yaml.safe_load(input_file)

def is_negative(field):
    # 'd$' is negative, all else
    return re.match('d$', field) is not None

def drop_positive(field):
    return re.sub('[cf]$', '', field)

def file_parser(data_file, key_start, key_end, record_definitions, formats, columns, sizes):
    '''
    Parse an ebcdic file according to:
    Parameters:
    -----------
    data_file: str, name of file to parse
    record definitions,
    record type -
    formats,
    columns
    and sizes


    data_file - str, name of the file to read and parse
    key_position - tuple, the start and end of the key value
    record_definition - dict: { 
                                <record_type_value>: (size: int, format: str, columns: list, encodings: list),
                                <record_type_value>: (size: int, format: str, columns: list, encodings: list),
                                }
                x.decode('cp424')
                x.hex()

        ** The last letter denotes the sign, C & F are positive, D is negative. For your program, check for negative (D) and if not, treat as positive.

        Example:
            {'1': (1200, '1s2s...', ['FIELD-TYPE-OIL', 'WELL-APINO', ...], [ )
    '''
    records = {}
    keys = list(record_definitions['record_types'].keys())
    for key in keys:
        records[key] = []
    
    # Read the key value position
    total_bytes_read = 0
    f = open(data_file, 'rb', buffering=0)
    field_type = f.read(key_end - key_start)
    total_bytes_read += key_end - key_start
    while len(field_type) > 0:
        # 1. parse key field, key value
        field_type_str = field_type.decode('cp424')
        if field_type_str not in keys:
            raise Exception(f'field record number {field_type_str} not supported. must be in {keys}')

        record_definition_position = record_definitions['record_types'][field_type_str]['record_definition_position']
        # 2. select structure from record type config
        rec = field_type + f.read(sizes[record_definition_position] - 1)
        total_bytes_read += sizes[record_definition_position] - 1
        rec = struct.unpack(formats[record_definition_position], rec)
        records[field_type_str].append(rec)
        # get next field
        field_type = f.read(key_end - key_start)
        total_bytes_read += key_end - key_start

    # 3. separate rows according to key value into N dataframes, combine into one dataframe
    return records


@click.command()
@click.option("--copybook-file", type=str)
@click.option("--data-file", type=str)
@click.option("--record-type-config-file", help='yaml file defining records for record_type field value', type=str)
def cobol_data_parser(copybook_file, data_file, record_type_config_file):

    # Get the symbol table for the Cobol copybook source code
    symbol_table = extract_structures(copybook_file)
    print(symbol_table)

    # Get configuration file for the key field and field types
    dataset_parameters = get_dataset_config(record_type_config_file)
    key_start = int(dataset_parameters['Shared-Field-Record-Type']['key_position'][0])
    key_end = int(dataset_parameters['Shared-Field-Record-Type']['key_position'][1])
    # Get the data from the EBCDIC input file.
    datasets = file_parser(data_file,
                           key_start,
                           key_end,
                           dataset_parameters,
                           symbol_table.struct_format,
                           symbol_table.columns,
                           symbol_table.sizes)
    print(f'length of datasets {len(datasets)}')


if __name__ == '__main__':
    cobol_data_parser()
