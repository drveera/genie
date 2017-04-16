#!/bin/env Rscript

args <- commandArgs(trailingOnly = TRUE)

dfmfile <- args[1]
outname <- args[2]
dfmfiles <- list.files(path = dirname(dfmfile), pattern = "*assoc", full.names = TRUE)

fnames <- c("SingleWald.assoc","SingleScore.assoc","SingleFirth.assoc","FisherExact.assoc","DominantFisherExact.assoc")
pnames <- c("Pvalue","PVALUE","Pvalue","PvalueTwoSide","PvalueTwoSide")

library(ggman)


plotlist <- list()
for (i in 1:length(dfmfiles)){
    ## determine the pvalue column based on the filename
    tname <- unlist(strsplit(dfmfiles[i], split = "\\."))
    tl <- length(tname)
    testname <- paste(tname[tl-1],tname[tl],sep=".")
    pvalue <- pnames[grep(testname,fnames)[1]]
    print(dfmfiles[i])
    print(pvalue)
    dfm <- read.table(dfmfiles[i], header = TRUE)
    dfm$ggP <- dfm[,pvalue]
    dfm <- dfm[!is.na(dfm$ggP),]
    dfm$id <- paste(dfm$CHROM,dfm$POS,dfm$REF,dfm$ALT,sep=":")
    threshold <- -log10(0.05/nrow(dfm))
    p1 <- ggman(gwas = dfm, snp = 'id', pvalue = 'ggP', bp = "POS", sigLine = threshold, title = basename(dfmfiles[i]), ymax = threshold + 1)
    dfmsub <- dfm[-log10(dfm$ggP) > threshold,]
    dfmsub <- dfmsub[! is.na(dfmsub$ggP),]
    print(dim(dfmsub))
    print(head(dfmsub))
    if (nrow(dfmsub)!=0){
        p1 <- ggmanLabel(p1,labelDfm = dfmsub,snp = 'id', label = 'id', size = 2, colour = "black")
    }
    plotlist[[i]] <- p1
}

pdf(outname)
for (i in plotlist){
    print(i)
}
dev.off()
