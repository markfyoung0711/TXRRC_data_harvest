1. to generate the Lexer, Parser and Listener for python3:

antlr4 -listener -Dlanguage=Python3 Cobol85.g4

generates these:

    Cobol85Lexer.py
    Cobol85Listener.py
    Cobol85Parser.py

There is a .g4 file for Cobol84Preprocessor but I did not find a need to use it.
It may have been handy for removing comments from the Cobol code, like what I say to do manually below, but I'm not sure.

1. subclass Cobol85Listener.py and 

1. to generate tree for the Oil Ledger copybook for TX RRC
    1. copy the COBOL code and post process the line numbers off of the end of the file.
    1. Put in the proper structure based on the ola_copybook.txt example

    pygrun -t Cobol85 startRule ola_copybook.txt

1. To generate the symbol table that can be used then for generating python dat structure:

* python cobol.py ola_copybook.txt
