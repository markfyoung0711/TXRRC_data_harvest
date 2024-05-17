# to generate tree for the Oil Ledger copybook for TX RRC
1. copy the COBOL code and post process the line nubmers off of the end of the file.
2. Put in the proper structure based on the ola_copybook.txt example

    pygrun -t Cobol85 startRule ola_copybook.txt

# To generate the symbol table that can be used then for generating python dat structure:

1. python cobol.py ola_copybook.txt
