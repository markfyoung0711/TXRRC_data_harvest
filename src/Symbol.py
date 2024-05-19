from dataclasses import dataclass
import copy

@dataclass
class Symbol:
    level: int = None
    name: str = None
    picture: str = None
    cardinality: int = None
    redefines: str = None
    occurs: int = None
    usage: str = None

    def __init__(self):
        pass

    def complete(self):
        return (self.name is not None) and (self.picture is not None)

    def reset(self):
        self.level = None
        self.name = None
        self.picture = None
        self.cardinality = None
        self.redefines = None
        self.occurs = None
        self.usage = None

@dataclass
class SymbolTable:

    def __init__(self):
        # a completed symbol table will be a table of tables.
        self.table = []
        self.current_level = None

    def add_level(self):
        self.table.append([])
        self.current_level = self.table[-1]

    def add_symbol(self, symbol):
        self.current_level.append(copy.deepcopy(symbol))

    def complete(self):
        return len(self.table) > 0

    def get(self):
        return self.table
