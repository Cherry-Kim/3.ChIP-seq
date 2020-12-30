####################################################################
# File Name: Chip-seq.py
# > Author: HyoYoung Kim
# > Mail: khy6021@gmail.com
###################################################################
#! /usr/bin/python

import os,glob,string,sys 
from rpy2 import robjects as ro
r = ro.r

def STEP0_ALIGN(REF,sample): 
	os.system('java -jar /home/hykim/program/Trimmomatic-0.36/trimmomatic-0.36.jar SE -threads 16 -phred33 '+sample+'.fastq.gz '+sample+'.trim.fq.gz ILLUMINACLIP:/home/hykim/program/Trimmomatic-0.36/adapters/TruSeq3-PE-2.fa:2:151:10:5:true LEADING:3 TRAILING:3 SLIDINGWINDOW:4:15 MINLEN:36') 
	os.system('/home/program/bowtie-1.2.3-linux-x86_64/bowtie -S -p 24 --best --strata -m 1 --chunkmbs 500 '+REF+' '+sample+'.trim.fq.gz '+sample+'.sam') 
	os.system('samtools view -bS '+sample+'.sam > '+sample+'.bam') 

	os.system('samtools sort '+sample+'.bam -o '+sample+'.sorted.bam')
	os.system('samtools index '+sample+'.sorted.bam')
	os.system('/home/hykim/program/deepTools/bin/bamCoverage -b '+sample+'.sorted.bam -o '+sample+'.bw')

def STEP1_PEAK_CALLING(sample): 
	os.system('/home/hykim/program/MACS2-2.0.10.20130731/bin/macs2 callpeak -t '+sample+'.bam -f BAM --name '+sample+' -g mm -B -q 0.05') 

def STEP2_PEAK_ANNOTATION(sample,REF,GTF): 
	os.system('grep -v "#" '+sample+'_peaks.xls | sed -n "3, \$p" | awk -F "\t" \'{print $10 "\t" $1 "\t" $2 "\t" $3 "\t" "+"}\' > '+sample+'.input.bed') 
	os.system('perl /home/program/homer/bin/annotatePeaks.pl '+sample+'.input.bed '+REF+' '+' -gtf '+GTF+' > '+sample+'_annotations.txt') 

def STEP3_DIFFBIND():
	r.source("ChIPseeker_DiffBind.R")

def Main():
	REF='/home/program/homer/data/genomes/mm10/'
	GTF='/home/hykim/ChIP-seq/REF/mm10.refGene.gtf'
	PATH='/home/hykim/ChIP-seq/test/'
	file_list=os.listdir(PATH)
	fq_list= [file for file in file_list if file.endswith(".gz")]
#        for fname in fq_list:
#                sample=string.split(fname,'.')[0]
#		STEP0_ALIGN(REF,sample)

#	bam_list= [file for file in file_list if file.endswith(".bam")]
#        for fname in bam_list:  
#                sample=string.split(fname,'.bam')[0] 
#		STEP1_PEAK_CALLING(sample)		
#		STEP2_PEAK_ANNOTATION(sample,REF,GTF)
	STEP3_DIFFBIND()
Main()
