#! /usr/bin/python3

import csv
import os
import unicodedata
import re
import itertools

# Define unicode control chars
all_chars = (chr(i) for i in range(os.sys.maxunicode))
control_chars = chr(0x22)   # double quote
control_chars += chr(0x27)  # single quote
control_chars += chr(0x2c)  # comma
control_chars += ''.join(map(chr, itertools.chain(range(0x00,0x20), range(0x7f,0xa0))))

control_char_re = re.compile('[%s]' % re.escape(control_chars))

def remove_control_chars(s):
    return control_char_re.sub('', s)

def clean_file(csv_input_filename):
    if os.path.isfile(csv_input_filename):
        try:
            with open (csv_input_filename, 'r') as csv_input_file:
                csv_reader = csv.reader(csv_input_file)
                
                csv_output_filename = csv_input_filename[:-4] + '_CLEANED.csv'
                
                with open (csv_output_filename, 'w') as csv_output_file:
                    csv_writer = csv.writer(csv_output_file)
                    for row in csv_reader:
                        new_row = []

                        for column in row:
                            new_row.append(remove_control_chars(column))

                        # Remove final element if it is empty
                        if new_row[-1] == '':
                            del new_row[-1]
                        
                        csv_writer.writerow(new_row)
        except Exception as e:
            print('There was an error: %s' % str(e))

    else:
        print("Input file not found!")
    
    return

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="A file of float values in a column")

    args = parser.parse_args()

    clean_file(args.filename)