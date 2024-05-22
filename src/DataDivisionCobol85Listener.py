'''

The purpose of this program is to build a data structure that we can use to generate
the proper python reader code for the Cobol File section being parsed.

'''

from antlr4 import ParseTreeListener, ParserRuleContext
from Cobol85Listener import Cobol85Listener
from Cobol85Parser import Cobol85Parser
from Symbol import Symbol, SymbolTable

# We will build the symbol table, with a row for each Level 01 set of symbols.
'''
current_symbol will be a dict and will represent the current symbol being built for the symbol table.
when the code has all it needs for a valid symbol, it will add the current_symbol dict to the symbol_table

current_symbol keys:
    "symbol_name", the name of the cobol variable
    "picture", the type of the cobol variable. e.g. '9', '99', 'X' 'S9', 'V99'
    "cardinality", the cardinality (optional)
    "redefines", the field being redefined (optional)
    "occurs", the number of times the field definition occurs

    Example of redefines and occurs:

    Level:03 Name:COUNTY Type: PIC 9 Cardinality 18
    Level:03 Name:COUNTIES Type: PIC 9 Cardinality 3 Redefines: REDEFINES COUNTY Occurs OCCURS 6

    So COUNTIES is "like" an array with 6 elements 3-bytes long each for a total byte-length of 18
    and COUNTIES redefines the COUNTY variable

So a readable version of the COBOL parsed is as follows.
Repeated Level 01's within the same file definition act as a "union" (as in C) of the byte structure.

Level:01 Name:FIELD-MAST
  Level:02 Name:OIL-CODES
   Level:03 Name:TYPE-REC Type: PIC 9
   Level:03 Name:DIST Type: PIC 999
   Level:03 Name:FIELD Type: PIC 9 Cardinality 8
   Level:03 Name:OPR Type: PIC 9 Cardinality 6
   Level:03 Name:LEASE Type: PIC 9 Cardinality 5
   Level:03 Name:LSE-FILLER Type: PIC 99
   Level:03 Name:OFFSHORE Type: PIC 9
  Level:02 Name:FIELD-DATA
   Level:03 Name:F-NAME Type: PIC X Cardinality 32
   Level:03 Name:COUNTY Type: PIC 9 Cardinality 18
   Level:03 Name:COUNTIES Type: PIC 9 Cardinality 3 Redefines: REDEFINES COUNTY Occurs OCCURS 6
   Level:03 Name:DISC-DATE Type: PIC 9 Cardinality 8
   Level:03 Name:D-DATE Redefines: REDEFINES DISC-DATE
     Level:05 Name:DSC-CCYY Type: PIC 9 Cardinality 4
     Level:05 Name:DSC-CCYY-REDF Redefines: REDEFINES DSC-CCYY
       Level:07 Name:DSC-CC Type: PIC 99
       Level:07 Name:DSC-YR Type: PIC 99
     Level:05 Name:DSC-MO Type: PIC 99
     Level:05 Name:DSC-DAY Type: PIC 99
   Level:03 Name:F-DEPTH Type: PIC 9 Cardinality 5
   Level:03 Name:O-GRAV Type: PIC 999



'''

current_symbol = Symbol()
global_symbol_table = SymbolTable()

def visit_to_generate_symbol_table(ctx:ParserRuleContext):

    numChildren = ctx.getChildCount()

    if numChildren == 0:
        # terminal, and we don't care about them b/c they will have been processed below
        return

    elif 'DataDescriptionEntryFormat1Context' in str(type(ctx)):

        '''
        Process tree like this (this is a tree structure from grun:

               (fileSection FILE SECTION .\n
                  (fileDescriptionEntry FD
                     (fileName
                        (cobolWord TXOilLedgerFile)) .\n
                     (dataDescriptionEntry
                        (dataDescriptionEntryFormat1 01 <<<<----- we care about these.
                           (dataName
                              (cobolWord FIELD-MAST)) .\n          ))
                     (dataDescriptionEntry
                        (dataDescriptionEntryFormat1 02 <<<<----- we care about these.
                           (dataName
                              (cobolWord OIL-CODES)) .\n              ))
                     (dataDescriptionEntry
                        (dataDescriptionEntryFormat1 03 <<<<----- we care about these.
                           (dataName
                              (cobolWord TYPE-REC))
                           (dataPictureClause PIC
                              (pictureString
                                 (pictureChars
                                    (integerLiteral 9)))) .\n              ))
                    ...

        N.B. Cannot ignore things w/o Picture Clause (PIC) because they could be redefines

        The following has no picture information but does indicate that it is redefining
        another field.

                     (dataDescriptionEntry
                        (dataDescriptionEntryFormat1 03
                           (dataName
                              (cobolWord D-DATE))
                           (dataRedefinesClause REDEFINES
                              (dataName
                                 (cobolWord DISC-DATE))) .\n                  ))
        '''


        if ctx.INTEGERLITERAL() is not None and ctx.dataName() is not None:

            _integer_literal = int(ctx.INTEGERLITERAL().getText())
            indent_chars = int(_integer_literal) * ' '
            _data_name = ctx.dataName().getText()

            # Flush current symbol to start building a new one
            if _integer_literal == 1:
                global_symbol_table.add_level()

            current_symbol.reset()
            current_symbol.name = _data_name
            current_symbol.level = _integer_literal

            # PIC
            _picture = []
            if len(ctx.dataPictureClause()) > 0:
                for cindex in ctx.dataPictureClause():
                    cardinality_seen = False
                    for counter, pindex in enumerate(cindex.pictureString().pictureChars()):
                        # will be: 9, (, 06, ), with only the 9 and 06 being integerLiteral
                        integer_literal = pindex.integerLiteral()
                        if integer_literal is not None:
                            integer_text = integer_literal.getText()
                            if cardinality_seen:
                                # this is a cardinality number
                                _picture.append('Cardinality')
                                _picture.append(integer_text)
                                current_symbol.cardinality = integer_text
                            else:
                                # this is a PIC number
                                current_symbol.picture = integer_text
                                _picture.append(integer_text)
                        else:
                            cardinality_check = pindex.getText()
                            if cardinality_check == '(':
                                cardinality_seen = True
                                continue
                            elif cardinality_check == ')':
                                cardinality_seen = False
                                continue
                            else:
                                integer_text = pindex.getText()
                                current_symbol.picture = integer_text
                                _picture.append(integer_text)

            _picture_string = ''
            if len(_picture) > 0:
                _picture_string = ' Type: PIC ' + ' '.join(_picture)

            # data usage
            _data_usage = []
            if len(ctx.dataUsageClause()) > 0:
                for cindex in ctx.dataUsageClause():
                    if (result := cindex.BINARY()) is not None:
                        _data_usage.append(result.getText())
                    if (result := cindex.BIT()) is not None:
                        _data_usage.append(result.getText())
                    if (result := cindex.COMP()) is not None:
                        _data_usage.append(result.getText())
                    if (result := cindex.COMP_1()) is not None:
                        _data_usage.append(result.getText())
                    if (result := cindex.COMP_2()) is not None:
                        _data_usage.append(result.getText())
                    if (result := cindex.COMP_3()) is not None:
                        _data_usage.append(result.getText())
                    if (result := cindex.COMP_4()) is not None:
                        _data_usage.append(result.getText())
                    if (result := cindex.COMP_5()) is not None:
                        _data_usage.append(result.getText())
                    if (result := cindex.COMPUTATIONAL()) is not None:
                        _data_usage.append(result.getText())
                    if (result := cindex.COMPUTATIONAL_1()) is not None:
                        _data_usage.append(result.getText())
                    if (result := cindex.COMPUTATIONAL_2()) is not None:
                        _data_usage.append(result.getText())
                    if (result := cindex.COMPUTATIONAL_3()) is not None:
                        _data_usage.append(result.getText())
                    if (result := cindex.COMPUTATIONAL_4()) is not None:
                        _data_usage.append(result.getText())
                    if (result := cindex.COMPUTATIONAL_5()) is not None:
                        _data_usage.append(result.getText())
                    if (result := cindex.CONTROL_POINT()) is not None:
                        _data_usage.append(result.getText())
                    if (result := cindex.DATE()) is not None:
                        _data_usage.append(result.getText())
                    if (result := cindex.DISPLAY()) is not None:
                        _data_usage.append(result.getText())
                    if (result := cindex.DISPLAY_1()) is not None:
                        _data_usage.append(result.getText())
                    if (result := cindex.DOUBLE()) is not None:
                        _data_usage.append(result.getText())
                    if (result := cindex.EVENT()) is not None:
                        _data_usage.append(result.getText())
                    if (result := cindex.FUNCTION_POINTER()) is not None:
                        _data_usage.append(result.getText())
                    if (result := cindex.INDEX()) is not None:
                        _data_usage.append(result.getText())
                    if (result := cindex.KANJI()) is not None:
                        _data_usage.append(result.getText())
                    if (result := cindex.LOCK()) is not None:
                        _data_usage.append(result.getText())
                    if (result := cindex.NATIONAL()) is not None:
                        _data_usage.append(result.getText())
                    if (result := cindex.PACKED_DECIMAL()) is not None:
                        _data_usage.append(result.getText())
                    if (result := cindex.POINTER()) is not None:
                        _data_usage.append(result.getText())
                    if (result := cindex.PROCEDURE_POINTER()) is not None:
                        _data_usage.append(result.getText())
                    if (result := cindex.REAL()) is not None:
                        _data_usage.append(result.getText())
                    if (result := cindex.TASK()) is not None:
                        _data_usage.append(result.getText())
                    if (result := cindex.USAGE()) is not None:
                        _data_usage.append(result.getText())
                    if (result := cindex.IS()) is not None:
                        _data_usage.append(result.getText())
                    if (result := cindex.TRUNCATED()) is not None:
                        _data_usage.append(result.getText())
                    if (result := cindex.EXTENDED()) is not None:
                        _data_usage.append(result.getText())
                if len(_data_usage) > 0:
                    current_symbol.usage = _data_usage

            # REDEFINES
            _redefines = []
            if len(ctx.dataRedefinesClause()) > 0:
                for cindex in ctx.dataRedefinesClause():
                    _redefines.append(cindex.REDEFINES().getText())
                    redefines_symbol = cindex.dataName().getText()
                    current_symbol.redefines = redefines_symbol
                    _redefines.append(redefines_symbol)
            _redefines_string = ''
            if len(_redefines) > 0:
                _redefines_string = ' Redefines: ' + ' '.join(_redefines)

            # OCCURS
            _occurs = []
            if len(ctx.dataOccursClause()) > 0:
                for cindex in ctx.dataOccursClause():
                    _occurs.append(cindex.OCCURS().getText())
                    occurs_number = str(cindex.integerLiteral().getText())
                    _occurs.append(occurs_number)
                    current_symbol.occurs = int(occurs_number)
            _occurs_string = ''
            if len(_occurs) > 0:
                _occurs_string = ' Occurs ' + ' '.join(_occurs)

            print(f'{indent_chars}Level:{_integer_literal} Name:{_data_name}{_picture_string}{_redefines_string}{_occurs_string}')
        else:
            raise Exception('unexpected result')

        if current_symbol.complete():
            global_symbol_table.add_symbol(current_symbol)

        return

    for idx in range(0, ctx.getChildCount()):
        visit_to_generate_symbol_table(ctx.getChild(idx))


# This class defines a complete listener for a parse tree produced by Cobol85Parser.
class DataDivisionCobol85Listener(Cobol85Listener):

    def __init__(self):
        '''
        Create a Cobol85Listener, specialize it to walk the File Section, generate symbol table and return it

        Parameters:
        -----------
        symbol_table: SymbolTable, this will be filled in and can then be returned.
        '''

        super().__init__()
        self.symbol_table = None

    # Enter a parse tree produced by Cobol85Parser#fileSection.
    def enterFileSection(self, ctx:Cobol85Parser.FileSectionContext):
        visit_to_generate_symbol_table(ctx)
        self.symbol_table = global_symbol_table
        self.symbol_table.cleanup_redefined()
        self.symbol_table.finalize()

    def get_symbol_table(self):
        return self.symbol_table
