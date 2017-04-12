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

p1 <- ggplot(sumdfm, aes(threshold,pheno)) + geom_tile(aes(fill = R2)) +
    theme(axis.text.x=element_text(angle=90, hjust=1)) +
    scale_fill_gradient(low = "white", high = "red")

ggsave(outname)
