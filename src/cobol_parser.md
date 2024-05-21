# Impetus
Each of the RRC datasets has a Cobol copybook.
Rather than interpret and write custom parsing code, it should be
possible to write a general-purpose tool to read the copybook and
generate the python code needed to parse the raw EBCDIC file (after
reading one into a bytearray).

# Ideas
## Generate a handgrown parser
The first idea was to write a parser that would use RE to figure
out sizes of fields, etc.  But that proved to be to much work.
The work was in understanding the lexical and parsing rules.
Surely someone else had done the work to provide a COBOL grammar.

## ANTLR4 Parser/Lexer
The second idea was to use an already-written grammar file
to generate a lexer and parser that could be customized.
I found ANTLR4, did some learning on YouTube about the listener
pattern, and customized a Listener to lex/parse and interpret the
items in the Data Division.  Way less work to understand COBOL
but still work to derive sizes from PICTURE (PIC), Cardinality,
Occurs, Redefines, etc.  Nonetheless, much less work than
writing a parser from scratch and "re-inventing the wheel".

# Result
These are the steps to generate the Lexer, Parser, Listener and
customize the Listener.

1. to generate the Lexer, Parser and Listener for python3:
`antlr4 -listener -Dlanguage=Python3 Cobol85.g4`
Generates these:
`Cobol85Lexer.py Cobol85Listener.py Cobol85Parser.py`
</code>
1. Preprocessor?
There is a .g4 file for Cobol84Preprocessor but I did not find a use for it.
It may have been handy for removing comments from the Cobol code, like what I say to do manually below, but I'm not sure.
1. subclass Cobol85Listener.py and add the listener/visitor code that will
be able to build a Symbol and SymbolTable.  Write a wrapper `cobol.py` program
that will run the Lexer, Parser, and customized Listener so that the Symbol(s)
and SymbolTable can be built.  The listener should fill in the symbol and symbol table
objects for later inspection for building the python [struct](https://docs.python.org/3/library/struct.html) formats
1. copy the copybook into a Cobol program and make the program complete by
adding other required divisions
`ola_copybook.cobol` is the resulting file from this step
1. to generate tree for the Oil Ledger copybook for TX RRC
    1. copy the COBOL code and post process the line numbers off of the end of the file.
    1. Put in the proper structure based on the ola_copybook.txt example
    It helped to generate a tree for the program<br>`pygrun -t Cobol85 startRule ola_copybook.cobol`
1. To generate the symbol table that can be used then for generating python dat structure:
    <code>python cobol.py ola_copybook.txt</code>

