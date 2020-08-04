# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 14:27:23 2020

@author: MBelobraydic
"""

#import pandas as pd
#import ebcdic
import codecs
from dbf900_main import parse_record
from dbf900_layouts import dbf900_layout
from dbf900_formats import pic_yyyymmdd, pic_yyyymm, pic_latlong, pic_coord, pic_numeric, pic_any





def main():
    file = r'C:\PublicData\Texas\TXRRC\index\dbf900.ebc' ##Local storage location
    ##file origin: ftp://ftpe.rrc.texas.gov/shfwba/dbf900.ebc.gz
    
    print('opening',file)
    with open(file, 'rb') as ebcdicfl: #Reads the .ebc file
        data = ebcdicfl.read()
    
    print('decoding...')
    ascii_txt = codecs.decode(data, 'cp1140') #decodes the entire .ebc file to ascii
    ##This decoding method still leaves a few uncoded "/x0" type characters
    
    split_records = []
    
    block_size  = 247 ##block size for each record in the file
    ##Unknown if this holds true for all versions of this file or for other files on TXRRC
    
    print('separating records...')
    for index in range(0, len(ascii_txt), block_size): ##Creates an array for all records in the file
        split_records.append(ascii_txt[index : index + block_size])
        
    """
    ##Section for testing the outputs
    """
    API = None
    api_check = None
    ct = 0
    check = 0
    
    sample_records = split_records #[34000:65000] ## Used for testing to reduce number of records to run
    
    #while check <100:
    while api_check == API:
        record = sample_records[ct]
        
        if not API:
            api_check = '42'+record[2:10]
        
        if record.startswith('01'):
            API = '42'+record[2:10]
    
        startval = str(record[0:2])
        layout = dbf900_layout(startval)['layout']
        parsed_vals = parse_record(record, layout)


    
        #if startval =='08': ##currently reviewing results vs. original record. Use 01 through 28 to check results.
            #check+=1
        print(ct, API, parsed_vals)
            #print(record)
        print('--------------------------------------')
        ct+=1
    
    
    
    
if __name__ == '__main__': 
    main()