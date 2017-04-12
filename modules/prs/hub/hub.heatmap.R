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
mf <- function(x,sep){
    xsplit = strsplit(x,split = sep)
    xdfm <- as.data.frame(do.call(rbind,xsplit))
    res <- list()
    for (i in 1:ncol(xdfm)){
        if (!all(xdfm[,i] == xdfm[1,i])){
            res[[length(res)+1]] <- as.character(xdfm[,i])
        }
    }
    res <- as.data.frame(do.call(rbind,res))
    res <- apply(res,2,function(x) paste(x,collapse="_"))
    return(res)
}
sumdfm$pheno <- mf(sumdfm$pheno,sep = "_")

p1 <- ggplot(sumdfm, aes(threshold,pheno)) + geom_tile(aes(fill = R2)) +
    theme(axis.text.x=element_text(angle=90, hjust=1)) +
    scale_fill_gradient(low = "white", high = "red")

ggsave(outname)
