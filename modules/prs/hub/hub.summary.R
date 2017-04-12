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
sumdfm <- do.call(rbind, sumlist)
thold <- sumdfm$threshold
thold <- thold[!duplicated(thold)]
sumdfm$threshold <- factor(sumdfm$threshold, levels = thold[mixedorder(thold)])
sumpheno <- sumdfm[pheno == basename(outname)]
p1 <- ggplot(sumdfm,aes(threshold,R2, group = pheno)) + geom_line(alpha = 0.1) +
    theme(axis.text.x=element_text(angle=90, hjust=1)) +
    labs(x = "P Value Thresholds", y = "Nagelkerke-R-Squared", title = paste0(basename(outname),"r2.plot")) +
    geom_line(data = sumpheno, aes(colour = pheno))
ggsave(paste0(outname,"rsquaredValues.allpheno.pdf"))
