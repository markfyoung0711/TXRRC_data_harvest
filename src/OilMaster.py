import simplejson
from coboljsonifier.copybookextractor import CopybookExtractor
from coboljsonifier.parser import Parser
from coboljsonifier.config.parser_type_enum import ParseType


class OilMaster(object):
    '''Parser for TX RRC Oil Master
    2024 location: https://mft.rrc.texas.gov/link/c5081c77-d32c-4ded-9b33-5aca3833306c#

    This class will read the COBOL copy book format from the defining PDF and derive the Python structure.
    https://mft.rrc.texas.gov/link/c5081c77-d32c-4ded-9b33-5aca3833306c#
    https://mft.rrc.texas.gov/link/c5081c77-d32c-4ded-9b33-5aca3833306c is index location
    file name format in HTML output:  olf{district_number}I.ebc.gz, where district number is a fixed 3 digit number with leading padded zeros
        e.g. o

    Record and Field Definition: https://www.rrc.texas.gov/media/5mlpe0t2/ola013k.pdf
    '''

    def __init__(self, cobol_data_division_file):
        self.record_definition_uri = 'https://www.rrc.texas.gov/media/5mlpe0t2/ola013k.pdf'
        self.input_uri = 'https://www.rrc.texas.gov/media/5mlpe0t2/ola013k.pdf'
        self.format = None

        # Extracting copybook structure
        self.dict_structure = CopybookExtractor(cobol_data_division_file).dict_book_structure

        # Building a Parser
        self.parser = Parser(self.dict_structure, ParseType.FLAT_ASCII).build()

        pass

    def get_format(self):
        return self.dict_structure

    def parse(self, input_bytes):
        self.parser(input_bytes)
        return simplejson.dumps(self.parser.value)
