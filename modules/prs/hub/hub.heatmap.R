#!/bin/env Rscript

args <- commandArgs(trailingOnly = TRUE)

sumfiles <- args[1]
outname <- args[2]

sumfiles <- readLines(sumfiles)

library(data.table)
library(ggplot2)
library(gtools)


sumlist <- list()
for(i in 1:length(sumfiles)){
    sumlist[[i]] <- fread(sumfiles[i], header = TRUE)    
}
#sumlist <- lapply(sumlist, function(x) x[x$R2 == max(x$R2),])
sumdfm <- do.call(rbind, sumlist)
sumdfm <- sumdfm[! is.na(sumdfm$pvalue),]
threshold <- as.character(sumdfm$threshold)
threshold <- threshold[!duplicated(threshold)]
sumdfm$threshold <- factor(sumdfm$threshold, levels = threshold[mixedorder(threshold)])
sumdfm$R2disc <- cut(sumdfm$R2, breaks = c(0,0.01,0.02,0.04,0.06,0.08,0.1,0.15,0.2), right = FALSE)
sumdfm$pvalue1 <- cut(sumdfm$pvalue, breaks = c(0,0.000001,0.00001,0.0001,0.001,0.01,0.05,1))
#p1 <- ggplot(sumdfm, aes(threshold,pheno)) + geom_tile(aes(fill = R2disc)) +
#    theme(axis.text.x=element_text(angle=90, hjust=1)) + scale_fill_brewer(palette = "Purples")

p2 <- ggplot(sumdfm, aes(threshold,pheno)) + geom_tile(aes(fill = pvalue1)) +
    geom_text(aes(label = round(R2,3)), size = 2) +
    theme(axis.text.x=element_text(angle=90, hjust=1)) + scale_fill_brewer(palette = "Purples", direction = -1) +
    scale_x_discrete(labels = c("S1" = "<5e-8","S2" = "<1e-6","S3" = "<1e-4","S4" = "<0.001","S5" = "<0.01","S6" = "0.05","S7" = "0.1","S8" = "0.2",
                                "S9" = "0.5","S10" = "1")) +
    theme(axis.text.x = element_text(angle = 90, hjust = 1))

pdf(outname, width = 12, height = 5)
#print(p1)
print(p2)
dev.off()


