BiocManager::install("DiffBind")
library(DiffBind)
BiocManager::install("tidyverse")
library(tidyverse)

#Reading in Peaksets
samples <- read.csv("sampleSheet.csv")
DBdata <- dba(sampleSheet=samples)


### STEP1. Counting reads
#This step is to calculate a binding matrix based on the read counts for samples.
DBdata <- dba.count(DBdata)
#As you can see all the samples are using the same length (Intervals) consensus peakset. 
#The last column tells us the Fraction of Reads In Peaks (FRiP). This is the proportion of reads that overlap with peaks in the consensus peakset, based on this value we can tell the enrichment of each sample.

### STEP2. Establishing contrast
DBdata <- dba.contrast(DBdata, categories=DBA_CONDITION, minMembers = 2)
#minMembers parameter to 2 (default is 3) : two samples in each condition

### STEP3.Differential binding analysis
#DBdata <- dba.analyze(DBdata)
DBdata <- dba.analyze(DBdata, method=DBA_EDGER)
#res_deseq <- dba.report(DBdata, method=DBA_EDGER)
res_deseq <- dba.report(DBdata, method=DBA_DESEQ2, contrast = 1, th=1)
out <- as.data.frame(res_deseq)
write.table(out, file="test_report.txt", sep="\t", quote=F, row.names=F)

#The heatmap shows the number of intervals (peaks) in the different samples.
pdf(file='heatmap.pdf')
dba.plotHeatmap(DBdata, contrast=1, correlations=FALSE)
dev.off()

#https://hbctraining.github.io/Intro-to-ChIPseq/lessons/08_diffbind_differential_peaks.html