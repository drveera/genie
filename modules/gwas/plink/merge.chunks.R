#!/bin/env Rscript

args <- commandArgs(trailingOnly = TRUE)

chunklist <- args[1]
outfile <- args[2]
chunkfiles <- readLines(chunklist)

library(data.table)
mlist <- list()
for(i in 1:length(chunkfiles)){
  mlist[[i]] <- fread(chunkfiles[i])
}
mdfm <- do.call(rbind,mlist)
mdfm <- data.table(mdfm)
fwrite(mdfm,outfile,sep="\t",na="NA")

