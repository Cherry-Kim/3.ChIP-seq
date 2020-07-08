import string,sys,os,glob

fp=glob.glob('samplel.bam')

co=0
for fname in fp:
	co+=1
	print fname

	sample=fname.split('.')[0]
	os.system('samtools sort '+fname+' -o '+sample+'.sorted.bam')
	os.system('samtools index '+sample+'.sorted.bam')
	os.system('/home/hykim/program/deepTools/bin/bamCoverage -b '+sample+'.sorted.bam -o '+sample+'.bw')
