#!/usr/bin/env python
"""
this script converts a gtf file to a csv containing only the gene name coverage,FPKM and TPM

usage
python gtf2csv.py input.gtf > output.csv
"""

import csv
import sys

with open(sys.argv[1],'r') as csvfile:
    readCSV = csv.reader(csvfile, delimiter="\t")
    for row in readCSV:
        temp_list=[]

        if not row[0].startswith("#"):

            if row[2] == "transcript":

                info = row[8].split(';')

                temp_list.append(info[1].split('"')[1])#gene name
                temp_list.append(info[-4].split('"')[1])#coverage
                temp_list.append(info[-3].split('"')[1])#FPKM
                temp_list.append(info[-2].split('"')[1])#TPM
 		print ",".join(temp_list)
