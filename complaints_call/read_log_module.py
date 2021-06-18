#!/usr/bin/python

import xlsxwriter
from datetime import datetime
import os

class Read_mss_log:

    def __init__(self, mss_log_file):
        self.path_to_file = mss_log_file

    def txt_reader(self):
        with open(self.path_to_file, 'r') as file1:
            while True:
                # Get next line from file
                line = file1.readline()
                # if line is empty # end of file is reached
                if not line:
                    break
                if '*** UNKNOWN SUBSCRIBER ***' in line:
                    return 'UNKNOWN SUBSCRIBER'
            return 'KNOWN SUBSCRIBER'

if __name__ == '__main__':
    path_to_file = 'storage_txt_and_xlsx/test_file.txt'
    txt_reader_obj = Read_mss_log(path_to_file)
    txt_reader_obj.main()
