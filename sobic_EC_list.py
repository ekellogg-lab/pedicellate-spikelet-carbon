#!/usr/bin/env python
"""
This script takes a csv conaining the sorghum transcriptome and the TPM values from multiple tissues
and returns a csv containg only the genes associated with a specified set of EC values.

usage
python sobic_EC_list.py <input_TPM.csv> <EC_values_to_keep.csv> <EC_values_of_all_sorghum_genes.csv> 
"""
import sys

#initialize dictionary for gene IDs and TPM
TPM_dict = {}

#open csv of transcripts and expression levels
with open(sys.argv[1],'r') as f:
    for line in f:
        line = line.strip()
        if line.startswith("Transcript_ID"):
	   #print header of output file
            print line + ",EC"
        else:
	    #record IDs and TPM values in dictionary
            TPM_dict[line.split(",")[0]] = line

#initialize EC value list
EC_value = []

#open file containing EC numbers of interest and save in list
with open(sys.argv[2],'r') as f:
    for line in f:
        line = line.strip()
        EC_value.append(line.split(",")[0])

#open csv containing all sobic genes and their EC values
with open(sys.argv[3],'r') as f:
    for line in f:
        line = line.rstrip("\n")

        if len(line.split("\t")) >= 7:
            EC_list = line.split("\t")[7].split(",")
            for EC in EC_list:
		
		#compare EC number to list of important EC values
		# if it matches print out TPM values for that gene from dictionary
                if EC.strip('"') in EC_value:
                    if line.split("\t")[2] + ".v3.2" in TPM_dict:

                        print TPM_dict[line.split("\t")[2] + ".v3.2"] + "," + line.split("\t")[7].strip('"')

                    else:
                        print line.split("\t")[2]
