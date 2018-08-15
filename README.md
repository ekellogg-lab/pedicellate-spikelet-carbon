These scripts were used in the analysis of RNA-seq data in Aubuchon et al. 2018 (in prep)


-------------------------
gtf2csv.py takes the gtf output of stringtie and reformats it as a csv with the format:
gene_name,coverage,FPKM,TPM

usage
python gtf2csv input.gtf > output.csv

-------------------------
sobic_EC_list.py takes the full transcriptome in the csv format returned by gtf2csv.py and returns the genes that match a set list of EC numbers.
EC_values_of_all_sorghum_genes.txt should contain the gene ID in column 1 and EC numbers as a comma-delimited list in column 8.
We used Sbicolor_454_v3.1.1.annotation_info.txt from Phytozome 12.

usage
python sobic_EC_list.py input_TPM.csv EC_values_to_keep.csv EC_values_of_all_sorghum_genes.txt > output.csv


-------------------------
orthogroup_blast.py takes the tab delimited output of Orthofinder and blasts all of the Themeda triandria genes in an orthogroup against all of the Sorghum bicolor genes in the same group. 
If the Themeda gene's best hit is a sorghum gene contained in the first column of sobic_genes.csv both of the Themeda and Sorghum gene IDs are printed to the terminal in csv format.

Requires:
output of Orthofinder
cds of all Sorghum bicolor and Themeda triandria genes in fasta format
blast+

usage
python orthogroup_blast.py orthogroup_file.txt sobic_genes.csv cds_themeda.fa cds_sobic.fa > output.csv
-------------------------