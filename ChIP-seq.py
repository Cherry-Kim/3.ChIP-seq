import os,glob,string,sys

REF='/home/program/homer/data/genomes/mm10/'
GTF='mm10.refGene.gtf'
'''
co=0
fp=glob.glob('*.gz')
for fname in fp:
	co+=1
	a=string.split(fname,'.')
	Sample=a[0]
	print '### Sample',co,Sample
	os.system('java -jar /home/hykim/program/Trimmomatic-0.36/trimmomatic-0.36.jar SE -threads 16 -phred33 '+Sample+'.fastq.gz '+Sample+'.trim.fq.gz ILLUMINACLIP:/home/hykim/program/Trimmomatic-0.36/adapters/TruSeq3-PE-2.fa:2:151:10:5:true LEADING:3 TRAILING:3 SLIDINGWINDOW:4:15 MINLEN:36')

	os.system('bowtie -S -p 24 --best --strata -m 1 --chunkmbs 500 /home/hykim/ChIP-seq/REF/mm10 '+Sample+'.trim.fq.gz '+Sample+'.sam')
	os.system('samtools view -bS '+Sample+'.sam > '+Sample+'.bam')

print "Peak calling"
fp=glob.glob('/home/hykim/ChIP-seq/*.bam')
for fname in fp: 
	a=string.split(fname,'/')
	b=string.split(a[4],'.')
	sample=b[0]
	os.system('macs2 callpeak -t '+fname+' -f BAM --name '+sample+' -g mm -B -q 0.05')

print "### Peak annotation using HOMER ###"
fp=glob.glob('/home/hykim/ChIP-seq/Peak_calling/*_peaks.xls')
for fname in fp:
	print fname
	a=os.path.basename(fname)
	b=string.split(a,'.')
	sample=b[0]
	os.system('grep -v "#" '+fname+' | sed -n "3, \$p" | awk -F "\t" \'{print $10 "\t" $1 "\t" $2 "\t" $3 "\t" "+"}\' > '+sample+'.input.bed')

fp=glob.glob('*.input.bed')
for fname in fp:
	print fname	
	a=fname.split('.')
	sample=a[0]
	os.system('perl /home/program/homer/bin/annotatePeaks.pl '+fname+' '+REF+' '+' -gtf '+GTF+' > '+sample+'_annotations.txt')
'''

fp=glob.glob('2_GCN5_BLM.bam')
for fname in fp:
	sample=fname.split('.')[0]
	os.system('samtools sort '+fname+' -o '+sample+'.sorted.bam')
	os.system('samtools index '+sample+'.sorted.bam')
	os.system('/home/hykim/program/deepTools/bin/bamCoverage -b '+sample+'.sorted.bam -o '+sample+'.bw')	
