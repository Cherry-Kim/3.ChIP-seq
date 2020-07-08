import string,sys,glob

fpout=open('gene1.txt','w')
fp=glob.glob('*_annotations.txt')
for fname in fp:
	fp1=open(fname,'r')
	hd=fp1.readline()
	fpout.write(hd)

	for line in fp1:
		line_temp=line.split('\t')
		if 'gene1' == line_temp[15]:
			fpout.write(line)

fp.close()
fpout.close()
