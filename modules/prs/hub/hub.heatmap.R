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
threshold <- as.character(sumdfm$threshold)
threshold <- threshold[!duplicated(threshold)]
sumdfm$threshold <- factor(sumdfm$threshold, levels = threshold[mixedorder(threshold)])
sumdfm$R2disc <- cut(sumdfm$R2, breaks = c(0,0.01,0.05,0.1), right = FALSE)
p1 <- ggplot(sumdfm, aes(threshold,pheno)) + geom_tile(aes(fill = R2disc)) +
    theme(axis.text.x=element_text(angle=90, hjust=1)) + scale_fill_brewer(palette = "Purples")

ggsave(outname, width = 12, height = 5)
