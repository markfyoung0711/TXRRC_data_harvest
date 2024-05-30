import tempfile

import pytest

from cobol_data_parser import extract_structures


@pytest.fixture
def test_1_copybook_file_contents():
    '''
    return a file object that contains the text below.
    have it be temporary so that it goes away afterward
    '''

    file_text = '''
IDENTIFICATION DIVISION.

PROGRAM-ID. SHOW-STRUCTURE.

DATA DIVISION.
FILE SECTION.
FD oil_file.
01 FIELD-MAST.
    02 OIL-CODES.
        03 TYPE-REC PIC 9.
        03 DIST PIC 999.
        03 FIELD PIC 9(8).
        03 OPR PIC 9(6).
        03 LEASE PIC 9(5).
        03 LSE-FILLER PIC 99.
        03 OFFSHORE PIC 9.
          02 FIELD-DATA.
              03 F-NAME PIC X(32).
              03 COUNTY PIC 9(18).
              03 COUNTIES REDEFINES COUNTY
                          OCCURS 6 TIMES
                                  PIC 9(3).
              03 DISC-DATE PIC 9(8).
              03 D-DATE REDEFINES DISC-DATE.
                  05 DSC-CCYY PIC 9(4).
                  05 DSC-CCYY-REDF REDEFINES DSC-CCYY.
                      07 DSC-CC PIC 99.
                      07 DSC-YR PIC 99.
                  05 DSC-MO PIC 99.
                  05 DSC-DAY PIC 99.
              03 F-DEPTH PIC 9(5).
              03 O-GRAV PIC 999.
              03 F-TYPE PIC 9.
              03 MULT-RES PIC 9.
              03 F-LPB PIC 9.
              03 F-XMT PIC 9.
              03 PRT-AS-IS PIC 9.
              03 YARD PIC 9.
              03 T-CODES PIC 9(12).
              03 TEST-CODE REDEFINES T-CODES OCCURS 12 TIMES PIC 9.
              03 ALLOCATION-PERCNT01 PIC V99.
              03 ALLOCATION-CODEF01 PIC 99.
              03 ALLOCATION-PERCNT02 PIC V99.
              03 ALLOCATION-CODEF02 PIC 99.
              03 ALLOCATION-PERCNT03 PIC V99.
              03 ALLOCATION-CODEF03 PIC 99.
              03 RES-AMT PIC 9(6). 
              03 F-GOR PIC 9(6).
              03 F-LIMIT REDEFINES F-GOR.
                  05 F-GOR-CODE PIC 9.
                  05 F-GOR-AMT PIC 9(5).
              03 F-TOP PIC 9(5).
              03 F-MER REDEFINES F-TOP.
                  05 F-TOP-CODE PIC 9.
                  05 F-TOP-AMT PIC 9(4).
              03 F-NET PIC 9(6).
              03 F-NGOR REDEFINES F-NET.
                  05 F-NET-CODE PIC 9.
                  05 F-NET-AMT PIC 9(5).
              03 UNET PIC 999.
              03 TOL PIC 9999.
              03 TOLER REDEFINES TOL.
                  05 F-TOL-CODE PIC 9.
                  05 F-TOL-AMT PIC 999.
              03 SPAC PIC 9(8).
              03 SPAC1-2 REDEFINES SPAC.
                  05 SPAC1 PIC 9999.
                  05 SPAC2 PIC 9999.
              03 DIAG PIC 9999.
              03 CUM-PROD PIC S9(13) COMP-3.
              03 CASING PIC X(21).
              03 COL-HEAD PIC X.
              03 ALO-CODE PIC X.
              03 F-RMK1 PIC X(66).
              03 F-RMK2 PIC X(66).
              03 PERM-NO PIC X(5).
              03 SP-FHC PIC 9.
              03 AN-1 PIC X(66).
              03 AN-2 PIC X(59).
              03 F-OOIP PIC 9(08).
              03 FILLER1 PIC 9(07).
              03 FILLER2 PIC 9(15).
              03 FILLER3 PIC 9(13).
              03 F-MONTH OCCURS 14 TIMES.
                  05 FM-DATE PIC 9(6).
                  05 FM-DATE-REDF REDEFINES FM-DATE.
                      07 FM-CCYY PIC 9(4).
                      07 FM-CCYY-REDF REDEFINES FM-CCYY.
                          09 FM-CC PIC 99.
                          09 FM-YR PIC 99.
                      07 FM-MO PIC 99.
                  05 FM-PW PIC S9(3) COMP-3.
                  05 FM-AC PIC S999V9(4) COMP-3.
                  05 FILLER4 PIC 9(4).
                  05 FM-OTHC PIC 9.
                  05 FM-CHG PIC 9.
                  05 FM-PROD-FACT PIC S99V999 COMP-3.
                  05 FM-SPLIT-PROD-FACT PIC S99V999 COMP-3.
                  05 FM-SPLIT-PROD-FACT-DATE PIC 99.
                  05 FM-JOHN PIC 9.
                  05 FM-OTH PIC S99999999V9999999 COMP-3.
                  05 FILLER5 PIC X(15).
      01 LEASE-MAST REDEFINES FIELD-MAST.
          02 LSE-CODES.
              03 LEASE-REC-TYPE-REC PIC 9.
              03 LEASE-REC-DIST PIC XXX.
              03 LEASE-REC-FIELD PIC 9(8).
              03 LEASE-REC-OPR PIC 9(6).
              03 LEASE-REC-LEASE PIC 9(5).
              03 LEASE-REC-FILLER PIC XX.
              03 LEASE-REC-OFFSHORE PIC 9.
          02 LEASE-DATA.
              03 L-NAME PIC X(32).
              03 LSE-CO PIC 9(6).
              03 LEASE-CO REDEFINES LSE-CO.
                  05 L-CO-1 PIC 999.
                  05 L-CO-2 PIC 999.
              03 POGATH PIC X(5).
              03 PGGATH PIC X(5).
              03 OSPLIT PIC 9.
              03 GSPLIT PIC 9.
              03 OOGATH PIC X(5).
              03 OGGATH PIC X(5).
              03 OOPR PIC 9(6).
              03 BO-STATUS PIC S9(7) COMP-3.
              03 BG-STATUS PIC S9(7) COMP-3.
              03 MOVE-BAL PIC S9(7) COMP-3.
              03 PO-STATUS PIC S9(7) COMP-3.
              03 PG-STATUS PIC S9(7) COMP-3.
              03 SEC-REC PIC 9.
              03 CERT PIC 99.
              03 BATCH PIC X.
              03 L-LPB PIC 9.
              03 COMMINGLE-CD PIC 9.
              03 COMMINGLE PIC 9999.
              03 L-INFO PIC X(54).
              03 AD-BO-STATUS PIC S9(7) COMP-3.
              03 AD-BG-STATUS PIC S9(7) COMP-3.
              03 COMMINGLE-DATE PIC 9(6).
              03 COMMINGLE-DATE-REDF REDEFINES COMMINGLE-DATE.
                  05 COMMINGLE-CCYY PIC 9(4).
                  05 COMMINGLE-CCYY-REDF REDEFINES
                     COMMINGLE-CCYY.
                      07 COMMINGLE-CC PIC 99.
                      07 COMMINGLE-YR PIC 99.
                  05 COMMINGLE-MO PIC 99.
              03 L-RMCD PIC 9.
              03 L-RMDT PIC 9(6).
              03 L-RMDT-REDF REDEFINES L-RMDT.
                  05 L-RMDT-CCYY PIC 9(4).
                  05 L-RMDT-CCYY-REDF REDEFINES L-RMDT-CCYY.
                      07 L-RMCC PIC 99.
                      07 L-RMYR PIC 99.
                  05 L-RMMO PIC 99.
              03 SEV-CD-13 PIC 9.
              03 SEV-CD-14 PIC 9.
              03 CAS-RED.
                  05 L-CAS-SI-LTR-DTE PIC 9(6).
                  05 L-RED-RTE-DTE PIC 9(6).
              03 CAS-RED-A REDEFINES CAS-RED.
                  05 L-CAS-CCYY PIC 9(4).
                  05 L-CAS-CCYY-REDF REDEFINES L-CAS-CCYY.
                      07 L-CAS-CC PIC 99.
                      07 L-CAS-YR PIC 99.
                  05 L-CAS-MO PIC 99.
                  05 L-RED-CCYY PIC 9(4).
                  05 L-RED-CCYY-REDF REDEFINES L-RED-CCYY.
                      07 L-RED-CC PIC 99.
                      07 L-RED-YR PIC 99.
                  05 L-RED-MO PIC 99.
              03 L-EXC-TST PIC 9.
              03 L-RLTYCD PIC 9.
              03 L-ONE-WELL-LEASE PIC X.
                  88 ONE-WELL-ON-SCHEDULE VALUE 'Y'.
                  88 MULTIPLE-WELL-LEASE VALUE 'N'.
              03 L-PANHANDLE-GOR-EXC PIC X(01).
              03 L-PANHANDLE-GOR-AMT PIC 9(08)V9 COMP-3.
              03 FILLER6 PIC 9(04).
              03 L-MONTH OCCURS 12 TIMES.
                  05 L-MONTH-DATE PIC 9(6).
                  05 L-MONTH-DATE-REDF REDEFINES
                     L-MONTH-DATE.
                      07 L-MONTH-CCYY PIC 9(4).
                      07 L-MONTH-CCYY-REDF REDEFINES
                         L-MONTH-CCYY.
                          09 LM-CC PIC 99.
                          09 LM-YR PIC 99.
                      07 LM-MO PIC 99.
                  05 LM-SEV PIC 9.
                  05 LM-RETRO PIC 9.
                  05 LM-REC PIC 9.
                  05 LM-CHG PIC 9.
                  05 LM-ALLOW PIC S9(7) COMP-3.
                  05 LM-PROD PIC S9(7) COMP-3.
                  05 LM-FW PIC 999.
                  05 LM-OW PIC 999.
                  05 LM-PL PIC S9(7) COMP-3.
                  05 LM-PLC PIC 9.
                  05 LM-OTH PIC S9(7) COMP-3.
                  05 LM-OTHC PIC 9.
                  05 LM-STO PIC S9(7) COMP-3.
                  05 LM-GL PIC S9(9) COMP-3.
                  05 LM-GPROD PIC S9(9) COMP-3.
                  05 LM-GLIFT PIC S9(7) COMP-3.
                  05 LM-CSIL PIC 9.
                  05 LM-JOHN PIC 9.
                  05 LM-LTR-CODE PIC 9.
                  05 FILLER7 PIC 9(13).
                  05 FILLER8 PIC 9(13).
              03 FILLER9 PIC 9(04).
      01 MULTI-MAST REDEFINES FIELD-MAST.
          02 MULTI-CODES.
              03 MULTI-W-REC-TYPE-REC PIC 9.
              03 MULTI-W-REC-DIST PIC XXX.
              03 MULTI-W-REC-FIELD PIC 9(8).
              03 MULTI-W-REC-OPR PIC 9(6).
              03 MULTI-W-REC-LEASE PIC 9(5).
              03 MULTI-W-REC-FILLER PIC 99.
              03 MULTI-W-REC-OFFSHORE PIC 9.
          02 MULTI-DATA.
              03 M-RECORD PIC X(6).
              03 TYPEW PIC X.
              03 RESER PIC X(5).
              03 UNIT-YATES REDEFINES RESER.
                  05 UNIT-NO-I PIC X.
                  05 UNIT-VALUE PIC 9V999.
              03 M-COUNTY PIC 9(6).
              03 MULTI-CO REDEFINES M-COUNTY.
                  05 M-CO-1 PIC 999.
                  05 M-CO-2 PIC 999.
              03 M-TST-EFF PIC X.
              03 M-PNTR-1ST PIC 9(6).
              03 CAP PIC 9.
              03 PROD-WELL PIC 9(6).
              03 PI-WELLS REDEFINES PROD-WELL.
                  05 M-PROD PIC 999.
                  05 M-INJ PIC 999.
              03 MARG-WELL PIC 9(6).
              03 SM-WELLS REDEFINES MARG-WELL.
                  05 M-SHUT PIC 999.
                  05 M-MARG PIC 999.
              03 M-DEPTH PIC 9.
              03 M-PNTR-LST PIC 9(6).
              03 M-EXC-TEST PIC 9.
              03 FILLER10 PIC 9(6).
              03 M-WATER PIC 9(6).
              03 M-REMARK PIC X(55).
              03 MM-PRCNT PIC V999.
              03 FILLER11 PIC 9(11).
              03 FILLER12 PIC 9(11).
              03 M-MONTH OCCURS 14 TIMES.
                  05 M-MONTH-DATE PIC 9(6).
                  05 M-MONTH-DATE-REDF REDEFINES
                     M-MONTH-DATE.
                      07 M-MONTH-CCYY PIC 9(4).
                      07 M-MONTH-CCYY-REDF REDEFINES
                         M-MONTH-CCYY.
                          09 MM-CC PIC 99.
                          09 MM-YR PIC 99.
                      07 MM-MO PIC 99.
                  05 MM-CHG PIC 9.
                  05 MM-NO PIC 9.
                  05 MM-ALLOW PIC S9(7) COMP-3.
                  05 MM-ACODE PIC 9.
                  05 MM-TCODE PIC 9.
                  05 MM-LIMIT PIC S9(9) COMP-3.
                  05 MM-ALLOW2 PIC S9(7) COMP-3.
                  05 MM-ACODE2 PIC 9.
                  05 MM-TCODE2 PIC 9.
                  05 MM-LIMIT2 PIC S9(9) COMP-3.
                  05 MM-DATE2 PIC 99.
                  05 MM-ALLOW3 PIC S9(7) COMP-3.
                  05 MM-ACODE3 PIC 9.
                  05 MM-TCODE3 PIC 9.
                  05 MM-LIMIT3 PIC S9(9) COMP-3.
                  05 MM-DATE3 PIC 99.
                  05 MM-FORM-LCK PIC 9.
                  05 MM-SPACE1 PIC S9(7) COMP-3.
                  05 MM-KODE2 PIC 9.
                  05 MM-SPACE2 PIC S9(7) COMP-3.
                  05 MM-JOHN PIC 9.
                  05 FILLER13 PIC 9(09).
                  05 FILLER14 PIC 9(09).
      01 WELL-MAST REDEFINES FIELD-MAST.
          02 WELL-CODES.
              03 WELL-REC-TYPE-REC PIC 9.
              03 WELL-REC-DIST PIC XXX.
              03 WELL-REC-FIELD PIC 9(8).
              03 WELL-REC-OPR PIC 9(6).
              03 WELL-REC-LEASE PIC 9(5).
              03 WELL-REC-FILLER PIC 99.
              03 WELL-REC-OFFSHORE PIC 9.
          02 WELL-DATA.
              03 WELL-NO PIC X(6).
              03 W-TYPE-WELL PIC X(1).
              03 FILLER15.
                  05 W-UNIT-NO PIC X.
                  05 W-UNIT-VALUE PIC 9V999.
              03 W-KEY PIC 9.
              03 W-COUNTY PIC 999.
              03 PUMP PIC 9.
              03 PUMPX REDEFINES PUMP PIC X.
              03 W-SP PIC 9(5).
              03 W-NET PIC 9(6).
              03 W-NGOR REDEFINES W-NET.
                  05 W-N-CODE PIC 9.
                  05 W-N-AMT PIC 9(5).
              03 W-DEPTH PIC 9(5).
              03 SAND PIC 9(3).
              03 FROZEN PIC 9(5).
              03 PERF PIC 9(5).
              03 W-DATE PIC 9(8).
              03 WELL-D REDEFINES W-DATE.
                  05 WELL-D-CC PIC 99.
                  05 WELL-D-YR PIC 99.
                  05 WELL-D-MO PIC 99.
                  05 WELL-D-DAY PIC 99.
              03 EX-14B-CD PIC X.
              03 W-SUB-WELL PIC 9.
              03 W-SUB-WELL-ALPHA REDEFINES W-SUB-WELL
                            PIC X.
              03 W-NO-PROD-CD PIC 9.
              03 W-DELQ-FORM PIC 9.
              03 W-TST-EFF PIC X.
              03 W-EXC-TST PIC 9.
                  88 ONE-WELL-LEASE-EXCEPTION VALUE 5.
              03 W-WATER PIC 9(4).
              03 EX-14B-DATE PIC 9(6).
              03 EX-14B-DATE-REDF REDEFINES EX-14B-DATE.
                  05 EX-CC-14B PIC 99.
                  05 EX-YR-14B PIC 99.
                  05 EX-MO-14B PIC 99.
              03 W-RMKS PIC X(15).
              03 BONUS-AMT PIC 9(4).
              03 BONS REDEFINES BONUS-AMT.
                  05 BONUS-CD PIC 9.
                  05 BONUS PIC 999.
              03 FROZTSF PIC 999.
              03 W-WLSD PIC 9.
              03 W-TST-DT PIC 9(8).
              03 W-TEST-DATE REDEFINES W-TST-DT.
                  05 W-TST-CC PIC 99.
                  05 W-TST-YR PIC 99.
                  05 W-TST-MO PIC 99.
                  05 W-TST-DA PIC 99.
              03 W-DTE-LST-UTL PIC 9(6).
              03 W-DTE-LST-UTL-REDF REDEFINES W-DTE-LST-UTL.
                  05 W-DTE-LST-UTL-CC PIC 99.
                  05 W-DTE-LST-UTL-YY PIC 99.
                  05 W-DTE-LST-UTL-MM PIC 99.
              03 W-NEW-WB-EXC PIC X(01).
              03 W-NEW-WB-CONNECT-DATE PIC 9(8).
              03 W-NEW-WB-CONNECT-DATE-REDF REDEFINES
                 W-NEW-WB-CONNECT-DATE.
                  05 W-NEW-WB-CC PIC 99.
                  05 W-NEW-WB-YR PIC 99.
                  05 W-NEW-WB-MO PIC 99.
                  05 W-NEW-WB-DA PIC 99.
              03 W-14B2-TYPE-COVERAGE PIC X(01).
              03 W-14B2-APP-NO PIC 9(06).
              03 FILLER17 PIC 9(04).
              03 FILLER18 PIC 9(18).
              03 FILLER19 PIC 9(07).
              03 W-MONTH OCCURS 14 TIMES.
                  05 W-MONTH-DATE PIC 9(6).
                  05 W-MONTH-DATE-REDF REDEFINES W-MONTH-DATE.
                      07 WM-CC PIC 99.
                      07 WM-YR PIC 99.
                      07 WM-MO PIC 99.
                  05 WM-CHG PIC 9.
                  05 WM-NO PIC 9.
                  05 WM-ALLOW PIC S9(5) COMP-3.
                  05 WM-ACODE PIC X.
                  05 WM-TCODE PIC X.
                  05 WM-LIMIT PIC S9(7) COMP-3.
                  05 WM-ALLOW2 PIC S9(5) COMP-3.
                  05 WM-ACODE2 PIC X.
                  05 WM-TCODE2 PIC X.
                  05 WM-LIMIT2 PIC S9(7) COMP-3.
                  05 WM-DATE2 PIC 99.
                  05 WM-ALLOW3 PIC S9(5) COMP-3.
                  05 WM-ACODE3 PIC X.
                  05 WM-TCODE3 PIC X.
                  05 WM-LIMIT3 PIC S9(7) COMP-3.
                  05 WM-DATE3 PIC 99.
                  05 WM-FORM-LCK PIC 9.
                  05 WM-PGT PIC S999 COMP-3.
                  05 WM-TSWA PIC 9.
                  05 WM-EGT PIC S999 COMP-3.
                  05 WM-ESWA PIC 9.
                  05 WM-ACRE PIC S999V99 COMP-3.
                  05 WM-POTE PIC S9999V9 COMP-3.
                  05 WM-ACFT PIC S9(5) COMP-3.
                  05 WM-GOR PIC S9(5) COMP-3.
                  05 WM-OTRAN-CD PIC 9.
                  05 WM-POT PIC S999 COMP-3.
                  05 WM-EOT PIC S999 COMP-3.
                  05 WM-JOHN PIC 9.
                  05 WM-OOIP PIC 9(06).
                  05 FILLER20 PIC 9(03).

WORKING-STORAGE SECTION.
01 EndOfFile    PIC X VALUE 'N'.
01 WS-EOF-FLAG  PIC X VALUE 'N'.

PROCEDURE DIVISION.
    DISPLAY 'Start of Program'.
    OPEN INPUT TXOilLedgerFile
    PERFORM UNTIL WS-EOF-FLAG = 'Y'
        READ MyFile INTO PersonRecord
            AT END
                MOVE 'Y' TO WS-EOF-FLAG
            NOT AT END
                PERFORM ProcessRecord
        END-READ
    END-PERFORM
    CLOSE MyFile
    DISPLAY 'End of Program'.
    STOP RUN.

ProcessRecord.
    DISPLAY 'WM-DATE3: ' WM-DATE3
    DISPLAY 'F-TYPE: ' F-TYPE
    DISPLAY 'SPAC: ' SPAC
    DISPLAY '---------------------'.
    '''

    return file_text


def test_extract_structures(test_1_copybook_file_contents):
    tmp = tempfile.NamedTemporaryFile()
    with open(tmp.name, 'w') as f:
        f.write(test_1_copybook_file_contents)
        symbol_table = extract_structures(tmp.name)
        assert(len(symbol_table) == 4)
        assert(symbol_table.sizes[0] == 1200)
        assert(symbol_table.sizes[1] == 1200)
        assert(symbol_table.sizes[2] == 1200)
        assert(symbol_table.sizes[3] == 1200)
        result = symbol_table.find_table_level_symbol('WM-JOHN')
        symbol_info = 'Symbol: Level: 5, Name: WM-JOHN, Picture: 9, Size: 1, Raw Memory Slice: 241:242, Raw Memory Slice(1): 242:243'
        assert(symbol_info == str(result[2]))
        result = symbol_table.find_table_level_symbol('FIELD-MAST')
        assert(result[0] is None)
        result = symbol_table.find_table(0)
        assert(len(result) == 81)
        (table, level, symbol) = symbol_table.find_table_level_symbol('OIL-CODES')
        assert(symbol_table.find_table_level_symbol('CAS-RED') == (None, None, None))
        _, level, _ = symbol_table.find_table_level_symbol('L-CAS-SI-LTR-DTE')
        assert(level is None)
