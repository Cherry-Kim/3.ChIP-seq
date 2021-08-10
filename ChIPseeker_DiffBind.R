#! /usr/bin/env Rscript

ChIPseeker <- function(
	anno = "org.Mm.eg.db",
	sp = "mouse"
	) {
#	BiocManager::install(c("ChIPseeker","clusterProfiler","ggupset","TxDb.Mmusculus.UCSC.mm10.knownGene","org.Mm.eg.db","ReactomePA"))
	#library(TxDb.Hsapiens.UCSC.hg19.knownGene)
	library(ChIPseeker)
	library(clusterProfiler)
	library(ggupset)
	library(TxDb.Mmusculus.UCSC.mm10.knownGene)
	txdb <- TxDb.Mmusculus.UCSC.mm10.knownGene
	library(org.Mm.eg.db)
	library(ReactomePA)

	data <- dir(pattern = "*_peaks.xls")

	pdf('AnnoPie.pdf', paper='letter')
	for (i in 1:length(data)) {
		print(data[i])
		# ChIP profiling
		peak <- readPeakFile(data[i])
		peakAnno <- annotatePeak(peak, tssRegion=c(-3000, 3000), TxDb=txdb, annoDb=anno)
		plotAnnoPie(peakAnno)
	}
	dev.off()

	#Functional enrichment analysis
	pdf('Pathway.pdf', paper='letter')
	for (i in 1:length(data)) {
		peak <- readPeakFile(data[i])
		#peakAnno <- annotatePeak(peak, tssRegion=c(-3000, 3000), TxDb=txdb, annoDb=anno)
		#pathway1 <- enrichPathway(as.data.frame(peakAnno)$geneId, organism="mouse")
		gene <- seq2gene(peak, tssRegion = c(-1000, 1000), flankDistance = 3000, TxDb=txdb)
		pathway <- enrichPathway(gene, organism = sp)
		png(paste0(data[i],".png"), width=4000, height=5000, res=200)
		h <- dotplot(pathway)
		print(h)
		dev.off()

		#Functional profiles comparison
#		peakAnnoList <- lapply(peak, annotatePeak, TxDb=txdb, tssRegion=c(-3000, 3000), verbose=FALSE)
#		genes = lapply(peakAnno, function(i) as.data.frame(i)$geneId)
	}

}

DiffBind <- function(
	file = "sampleSheet2.csv",
	rep = 2,
	diff = DBA_ALL_METHODS 	##DBA_EDGER, DBA_DESEQ2
	) {
	#BiocManager::install(c("DiffBind","tidyverse")
	library(DiffBind)
	library(tidyverse)

	#Reading in Peaksets
	samples <- read.csv(file)
	DBdata <- dba(sampleSheet=samples)
	### STEP1. Counting reads: This step is to calculate a binding matrix based on the read counts for samples.
	DBdata <- dba.count(DBdata)
	### STEP2. Establishing contrast
	DBdata <- dba.contrast(DBdata, categories=DBA_CONDITION, minMembers = rep)
	### STEP3.Differential binding analysis
	DBdata <- dba.analyze(DBdata, method = diff)
	res_deseq <- dba.report(DBdata, method= diff)
	out <- as.data.frame(res_deseq)
	write.table(out, file="test_report.txt", sep="\t", quote=F, row.names=F)

#	pdf(file="Venn.pdf")
#	dba.plotVenn(DBdata, contrast = 1, method=diff)
#	dev.off()
}

#ChIPseeker()
DiffBind()
