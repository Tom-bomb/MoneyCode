# -*- coding: utf-8 -*-
"""
Created on Thu Dec 29 16:44:24 2022

@author: bomtu
"""

import csv
import sys
import os


TRANSACTION_DATE = 0
POST_DATE = 1
DESCRIPTION = 2
CATEGORY = 3
TYPE = 4
AMOUNT = 5
MEMO = 6

category_map = {
    'Health & Wellness':'Expenses:Medical Expenses',
    'Payment Thank You - Web':'Payment',
    'Food & Drink':'Expenses:Dining',
    'Gas':'Expenses:Auto:Fuel',
    'Personal':'Expenses:Miscellaneous',
    'Travel':'Expenses:Entertainment:Travel',
    'Shopping':'Expenses:Miscellaneous',
    'Automotive':'Expenses:Auto:Repair and Maintenance',
    'Groceries':'Expenses:Groceries',
    'Bills & Utilities':'Expenses:Utilities:Electric',
    'Entertainment':'Expenses:Entertainment:Recreation',
    'Professional Services':'Expenses:Bank Service Charge'
    }

gnu_header = 'Date,Num,Description,Transfer,R,Payment,Charge\n'
gnu_rows = []

def get_gnu_row(row):
    old_cat = row[CATEGORY]
    typ = row[TYPE]
    new_cat = category_map.get(old_cat)
    st = ''
    if new_cat is None and typ != 'Payment':
        print('Unmapped key: ' + old_cat + '; skipping.')
        print(row)
        return
    if typ == 'Payment':
        st = '{},,{},{},,{},\n'
        st = st.format(row[TRANSACTION_DATE], 
                        row[DESCRIPTION], 
                        'Assets:Discretionary Assets:Liquid Accounts', 
                        row[AMOUNT])
    else:
        amount = row[AMOUNT]
        st = '{},,{},{},,,{}\n'
        st = st.format(row[TRANSACTION_DATE], 
                        row[DESCRIPTION], 
                        new_cat, 
                        amount[1:])
    return(st)

def get_gnu_rows(reader):
    first = True
    for row in reader:
        if first:
            first = False
            continue
        st = get_gnu_row(row)
        if st:
            gnu_rows.append(st)
        else:
            return False
    return True

def write_gnu(output_file):
    with open(output_file, 'w') as f:
        f.write(gnu_header)
        f.writelines(gnu_rows)


def main(path_to_input_file, output_dir):
    in_basename  = os.path.basename(path_to_input_file)
    out_basename  = os.path.splitext(in_basename)[0]
    
    with open(path_to_input_file) as input:
        reader = csv.reader(input, delimiter=',')
        ret = get_gnu_rows(reader)
        if ret is False:
            return False
        write_gnu(output_dir + '/' + out_basename + '_gnu.csv')
    return True

if __name__ == '__main__':
    args = sys.argv
    if len(args) <= 1:
        print('provide input file')
        sys.exit(-1)
    ret = main(args[1], args[2])
    if ret:
        sys.exit(0)
    sys.exit(-1)