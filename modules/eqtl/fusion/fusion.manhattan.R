#!/bin/env Rscript

args <- commandArgs(trailingOnly = TRUE)

dfmfileslist <- args[1]
outpdf <- args[2]

dfmfiles <- readLines(dfmfileslist)

dfmlist <- list()
for (i in 1:length(dfmfiles)){
    d  <- read.table(dfmfiles[i], header = TRUE)
    d <- d[!is.na(d$TWAS.P),]
    dfmlist[[i]] <- d
}
#print(lapply(dfmlist,dim))
library(ggman)

saveRDS(dfmlist,"temp.RDS")
plotlist <- list()
for (i in 1:length(dfmlist)){
    d <- dfmlist[[i]]
    d$gene <- paste(d$ID,d$MODEL, sep = "_")
    sigline <- -log10(0.05/nrow(d))
    d1 <- d[-log10(d$TWAS.P) > sigline,]
    cat("plotting ",i,"\n")
    p <- ggman(d, snp = "gene", bp = "P0", pvalue = "TWAS.P", sigLine = sigline, invert = TRUE, invert.method = "beta", invert.var = "TWAS.Z", pointSize = 1)
               #title = basename(dfmfiles[[i]])) + theme(plot.title = element_text(size = 10))
    #if(nrow(d1)>0){
    #    p <- ggmanLabel(p, labelDfm = d1, snp = "gene", label = "gene", size = 2, type = "text", colour = "black")    
                                        #}
    p
    plotlist[[i]] <- p
    ggsave("temp.pdf")
}

pdf(outpdf, width = 7, height = 3)
for (i in 1:length(plotlist)){
    print(plotlist[[i]])
}
dev.off()
