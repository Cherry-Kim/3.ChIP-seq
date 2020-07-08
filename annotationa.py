import string,sys,glob

fpout=open('Ccl12.txt','w')
fp=glob.glob('*_annotations.txt')
for fname in fp:
	print '###Sample',fname

	fp=open(fname,'r')
	hd=fp.readline()
	fpout.write(hd)

	for line in fp:
		line_temp=line.split('\t')
		if 'Ccl12' == line_temp[15]:
			fpout.write(line)

fp.close()
fpout.close()
