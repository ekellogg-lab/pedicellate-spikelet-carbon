#!usr/bin/env python
"""
This script takes the tab delimited output of orthofinder and Themeda transcripts against the Sorghum genes in the same orthogroup
if the best it is one of the sorghum genes of interest included in a csv the themeda genes are recorded along with the best sorghum match.
fasta files for the themeda and sobic cds are required
usage
python orthogroup_blast.py orthogroup_file.txt sobic_genes.csv cds_themeda.fa cds_sobic.fa > out.csv
"""

import sys
import subprocess
import os

orthofile = sys.argv[1]
gene_list_file = sys.argv[2]
fasta_TT = sys.argv[3]
fasta_sobic = sys.argv[4]


#this function makes a temporary fasta file of genes in the orthogroup from the supplied cds for use in blasting
def make_fasta(names,infile,outfile):
	num = len(names)
	count = 0
	with open (infile,'r') as f:
		w = open(outfile,'w')
		Switch = False
		for line in f:
			if line.startswith('>'):
				line = line.split()
				
				if Switch == True:
					
					if line[0].strip('>.p') in names:
						w.write(line[0]+'\n')
						count +=1

					else:
						Switch = False
				else:
					
					if line[0].strip('>.p') in names:
                                                w.write(line[0]+'\n')
                                                count +=1
						Switch = True
			else:
				if Switch==True:
					w.write(line.strip('\n')+'\n')
		w.close()





out_dict ={}

sobic_list = []
FNULL = open(os.devnull, 'w')
#open the list of sorghum genes of interest and store in a list
with open(gene_list_file,'r')as f:
	for line in f:
		
		line = line.split(',')
		#add ".v3.2" so string matches orthogroup names
		line[0] = line[0].replace('.v3.2','')
		sobic_list.append(line[0])

#open the orthogroup tab delimited file and loop through groups
with open(orthofile,'r') as f:
	for line in f:
		
		line = line.strip('\n')
		line =line.split(',')
		TTs = []
		Sobics = []
		
		for gene in line:
			if gene.startswith('T'):
				TTs.append(gene)
			elif gene.startswith('So'):
				Sobics.append(gene.strip('.p'))
		
		if len(Sobics) == 1: # if only one gene no blast necessary
			for thing in TTs:
				if thing not in out_dict:
					out_dict[thing] = Sobics[0].strip('.p')
		else:
			if len(TTs) > 0: #if multiple perform blasts
				make_fasta(Sobics,fasta_sobic,"sobic_temp.fa")#make temp fasta of sobic
				command = "makeblastdb -dbtype prot -in sobic_temp.fa" #make temp blastdb
				subprocess.call(command,stdout=FNULL, stderr=subprocess.STDOUT, shell=True)
				for TT in TTs: #for each themeda gene in group
					x = [TT]

					make_fasta(x,fasta_TT,"TT_temp.fa") #make temp themeda fasta
					command1 = "blastp -query TT_temp.fa -db sobic_temp.fa -outfmt 6 -max_target_seqs 1 -out blast_temp.out" # blast command 
					subprocess.call(command1,shell=True)
					with open('blast_temp.out', 'r')as f: #check blast output
						for line in f:
							line =line.strip()
							line=line.split()
							if line[1].strip('.p\n') in sobic_list: # if best Sobic hit is in gene of interest file add themeda and sobic gene to dictionary
								if line[0] not in out_dict:
									out_dict[line[0]] = line[1].strip('.p')


#print dictionary as a csv
for thing in sorted(out_dict):
	print(thing + ',' + out_dict[thing])
