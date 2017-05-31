#!/bin/env Rscript

args <- commandArgs(trailingOnly = TRUE)

slist.file <- args[1]
outfile <- args[2]

slist <- readLines(slist.file)

library(data.table)
rslt <- list()
for (i in 1: length(slist)){
  rslt[[i]] <- fread(slist[i], header = TRUE)
}
rslt <- do.call(rbind, rslt)
rslt <- data.table(rslt)

fwrite(rslt,outfile, sep = "\t", na = "NA")
