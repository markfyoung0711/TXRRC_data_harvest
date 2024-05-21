import copy

import pandas as pd

computationals = set(['COMP-1', 'COMP-2', 'COMP-3', 'COMP-4', 'COMP-5',
                      'COMPUTATIONAL-1', 'COMPUTATIONAL-2', 'COMPUTATIONAL-3',
                      'COMPUTATIONAL-4', 'COMPUTATIONAL-5', 'COMPUTATIONAL'])

# native = '@' see python struct()
BYTE_ORDER = '@'

def is_computational(usage):

    return (usage is not None) and (len(set(usage).intersection(computationals)) > 0)

class Symbol:
    level: int = None
    name: str = None
    picture: str = None
    cardinality: int = None
    redefines: str = None
    occurs: int = None
    usage: str = None
    start: int = None
    end: int = None
    struct_format: str = None
    packed: bool = False

    def __init__(self):
        pass

    def complete(self):
        return (self.name is not None)

    def reset(self):
        self.level = None
        self.name = None
        self.picture = None
        self.cardinality = None
        self.redefines = None
        self.occurs = None
        self.usage = None
        self.size = None
        self.start = None
        self.end = None
        self.struct = None
        self.packed = False

    def create(symbol):
        new_symbol = copy.deepcopy(symbol)

        if new_symbol.cardinality is not None:
            new_symbol.cardinality = int(new_symbol.cardinality)

        # compute size.
        # 9's - count = 9 occurrences + cardinality
        size = 0
        if new_symbol.picture is not None and '9' in new_symbol.picture:
            nines_count = str(new_symbol.picture).count('9')
            if new_symbol.cardinality is None:
                size = nines_count
            else:
                if nines_count == 1:
                    size += new_symbol.cardinality
                elif nines_count > 1:
                    size = nines_count - 1 + new_symbol.cardinality

            # adjust for USAGE with computational (packed decimal)
            if is_computational(new_symbol.usage):
                new_symbol.packed = True
                if size % 2 > 0:
                    size = (size / 2) + 1
                else:
                    size = int(size / 2)

        # X's - count X's or use cardinality
        elif new_symbol.picture is not None and 'X' in new_symbol.picture:
            if new_symbol.cardinality is not None:
                size = new_symbol.cardinality
            else:
                size = new_symbol.picture.count('X')

        if new_symbol.occurs is not None:
            size *= int(new_symbol.occurs)

        new_symbol.size = int(size)

        new_symbol.create_format()

        return new_symbol

    def __str__(self):
        pr_level = None
        if self.level is not None:
            pr_level = f'Level: {self.level}'

        pr_name = None
        if self.name is not None:
            pr_name = f'Name: {self.name}'

        pr_picture = None
        if self.picture is not None:
            pr_picture = f'Picture: {self.picture}'

        pr_cardinality = None
        if self.cardinality is not None:
            pr_cardinality = f'Cardinality: {self.cardinality}'

        pr_redefines = None
        if self.redefines is not None:
            pr_redefines = f'Redefines: {self.redefines}'

        pr_occurs = None
        if self.occurs is not None:
            pr_occurs = f'Occurs: {self.occurs}'

        pr_usage = None
        if self.usage is not None:
            pr_usage = f'Usage: {self.usage}'

        pr_size = None
        if self.size is not None:
            pr_size = f'Size: {self.size}'

        pr_slice = None
        if self.start is not None and self.end is not None:
            pr_slice = f'Raw Memory Slice: {self.start}:{self.end}'

        pr_1_slice = None
        if self.start is not None and self.end is not None:
            pr_1_slice = f'Raw Memory Slice(1): {self.start+1}:{self.end+1}'

        pr_struct_format = None
        if self.struct_format is not None:
            pr_struct_format = f'Struct Format: {self.struct_format}'

        details = [pr_level, pr_name, pr_picture, pr_cardinality, pr_redefines, pr_occurs, pr_usage, pr_size, pr_1_slice, pr_slice, pr_struct_format]
        pr_details = [x for x in details if x is not None]
        pr_details = ', '.join(pr_details)

        return f"Symbol: {pr_details}"

    def create_format(self):
        if self.size > 0:
            self.struct_format = f'{self.size}s'

class SymbolTable:

    def __init__(self):
        # a completed symbol table will be a table of tables.
        self.table = []
        self.current_level = None
        self.redefined = set()
        self.struct_format = []

    def add_level(self):
        self.table.append([])
        self.current_level = self.table[-1]

    def add_symbol(self, symbol):
        complete_symbol = Symbol.create(symbol)
        if complete_symbol.redefines is not None:
            self.redefined.add(complete_symbol.redefines)
        self.current_level.append(complete_symbol)

    def cleanup_redefined(self):
        new_table = []
        for level in self.table:
            new_table.append([])
            for symbol in level:
                if symbol.name in self.redefined:
                    continue
                else:
                    new_table[-1].append(symbol)

        self.table = new_table

    def complete(self):
        return len(self.table) > 0

    def validate(self):
        pass

    def get(self):
        return self.table

    def __str__(self):
        _str = ''
        for counter, level in enumerate(self.table):
            _str += '\nLevel 01\n'
            for symbol in level:
                _str += str(symbol) + '\n'

            _str += f'\nSymbol table size: {self.sizes[counter]}'
            _str += f'\nSymbol table struct format: {self.struct_format[counter]}'

        if self.redefined:
            _str += f'\nRedefined symbols: {self.redefined}'

        return _str

    def finalize_sizes(self):
        '''compute whole size of level and compute individual offsets for a struct generation
        E.g.
        Symbol: Level: 2, Name: OIL-CODES, Size: 0 Offset: 0
        Symbol: Level: 3, Name: TYPE-REC, Picture: 9, Size: 1 Offset: 1
        Symbol: Level: 3, Name: DIST, Picture: 999, Size: 3 Offset: 4 
        Symbol: Level: 3, Name: FIELD, Picture: 9, Cardinality: 8, Size: 8 Start: 5 End: 13
        Symbol: Level: 3, Name: OPR, Picture: 9, Cardinality: 6, Size: 6 Offset: 18
        Symbol: Level: 3, Name: LEASE, Picture: 9, Cardinality: 5, Size: 5 Offset: 23
        Symbol: Level: 3, Name: LSE-FILLER, Picture: 99, Size: 2 Offset: 25
        Symbol: Level: 3, Name: OFFSHORE, Picture: 9, Size: 1
        Symbol: Level: 2, Name: FIELD-DATA, Size: 0
        '''
        self.sizes = []
        for level in self.table:
            size = 0
            for symbol in level:
                # for the symbol
                start = size
                size += symbol.size
                end = size
                symbol.start = start
                symbol.end = end
            self.sizes.append(size)

    def finalize_struct_format(self):
        '''
        visit each symbol that has a size or occurs and compute the format from the size.
        usually it will just be {size}s (or a string of size).
        when occurs appears in a level variable that groups several other fields then
        the format has to be repeated by the number of Occurs.



        Consider these levels (pseudo-Cobol code):
        Level:3 Name:F-MONTH Occurs OCCURS 14
          Level:5 Name:FM-DATE Type: PIC 9 Cardinality 6
          Level:5 Name:FM-DATE-REDF Redefines: REDEFINES FM-DATE 
            Level:7 Name:FM-CCYY Type: PIC 9 Cardinality 4 
            Level:7 Name:FM-CCYY-REDF Redefines: REDEFINES FM-CCYY
              Level:9 Name:FM-CC Type: PIC 99 
              Level:9 Name:FM-YR Type: PIC 99
            Level:7 Name:FM-MO Type: PIC 99
          Level:5 Name:FM-PW Type: PIC S9 Cardinality 3
          Level:5 Name:FM-AC Type: PIC S999V9 Cardinality 4
          Level:5 Name:FILLER4 Type: PIC 9 Cardinality 4 
          Level:5 Name:FM-OTHC Type: PIC 9
          Level:5 Name:FM-CHG Type: PIC 9
          Level:5 Name:FM-PROD-FACT Type: PIC S99V999
          Level:5 Name:FM-SPLIT-PROD-FACT Type: PIC S99V999 
          Level:5 Name:FM-SPLIT-PROD-FACT-DATE Type: PIC 99
          Level:5 Name:FM-JOHN Type: PIC 9
          Level:5 Name:FM-OTH Type: PIC S99999999V9999999
          Level:5 Name:FILLER5 Type: PIC X Cardinality 15
      Level:1 Name:LEASE-MAST Redefines: REDEFINES FIELD-MAST

        In the example, the Level 5, 7 9 variables from FM-DATE thorugh FILLER5
        get repeated 14 times.
        The resulting one-time format would be:

        Symbol: Level: 3, Name: F-MONTH, Occurs: 14, Size: 0, Raw Memory Slice(1): 501:501, Raw Memory Slice: 500:500
        Symbol: Level: 5, Name: FM-DATE-REDF, Redefines: FM-DATE, Size: 0, Raw Memory Slice(1): 501:501, Raw Memory Slice: 500:500
        Symbol: Level: 7, Name: FM-CCYY-REDF, Redefines: FM-CCYY, Size: 0, Raw Memory Slice(1): 501:501, Raw Memory Slice: 500:500
        Symbol: Level: 9, Name: FM-CC, Picture: 99, Size: 2, Raw Memory Slice(1): 501:503, Raw Memory Slice: 500:502
        Symbol: Level: 9, Name: FM-YR, Picture: 99, Size: 2, Raw Memory Slice(1): 503:505, Raw Memory Slice: 502:504
        Symbol: Level: 7, Name: FM-MO, Picture: 99, Size: 2, Raw Memory Slice(1): 505:507, Raw Memory Slice: 504:506
        Symbol: Level: 5, Name: FM-PW, Picture: S9, Cardinality: 3, Usage: ['COMP-3'], Size: 2, Raw Memory Slice(1): 507:509, Raw Memory Slice: 506:508   
        Symbol: Level: 5, Name: FM-AC, Picture: S999V9, Cardinality: 4, Usage: ['COMP-3'], Size: 4, Raw Memory Slice(1): 509:513, Raw Memory Slice: 508:512
        Symbol: Level: 5, Name: FILLER4, Picture: 9, Cardinality: 4, Size: 4, Raw Memory Slice(1): 513:517, Raw Memory Slice: 512:516
        Symbol: Level: 5, Name: FM-OTHC, Picture: 9, Size: 1, Raw Memory Slice(1): 517:518, Raw Memory Slice: 516:517
        Symbol: Level: 5, Name: FM-CHG, Picture: 9, Size: 1, Raw Memory Slice(1): 518:519, Raw Memory Slice: 517:518
        Symbol: Level: 5, Name: FM-PROD-FACT, Picture: S99V999, Usage: ['COMP-3'], Size: 3, Raw Memory Slice(1): 519:522, Raw Memory Slice: 518:521
        Symbol: Level: 5, Name: FM-SPLIT-PROD-FACT, Picture: S99V999, Usage: ['COMP-3'], Size: 3, Raw Memory Slice(1): 522:525, Raw Memory Slice: 521:524
        Symbol: Level: 5, Name: FM-SPLIT-PROD-FACT-DATE, Picture: 99, Size: 2, Raw Memory Slice(1): 525:527, Raw Memory Slice: 524:526
        Symbol: Level: 5, Name: FM-JOHN, Picture: 9, Size: 1, Raw Memory Slice(1): 527:528, Raw Memory Slice: 526:527
        Symbol: Level: 5, Name: FM-OTH, Picture: S99999999V9999999, Usage: ['COMP-3'], Size: 8, Raw Memory Slice(1): 528:536, Raw Memory Slice: 527:535 
        Symbol: Level: 5, Name: FILLER5, Picture: X, Cardinality: 15, Size: 15, Raw Memory Slice(1): 536:551, Raw Memory Slice: 535:550





        '''
        self.struct_format = []
        for level in self.table:
            struct_format = BYTE_ORDER
            self.struct_format.append([])
            for symbol in level:
                if symbol.struct_format is not None:
                    struct_format += symbol.struct_format
            self.struct_format[-1].append(struct_format)

    def finalize(self):
        self.finalize_sizes()
        self.finalize_struct_format()
