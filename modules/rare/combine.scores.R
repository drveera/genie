#!/bin/env Rscript

args <- commandArgs(trailingOnly = TRUE)

lst.file <- readLines(args[1])
outfile <- args[2]

library(data.table)

lst <- list()
for (i in 1:length(lst.file)){
    lst[[i]] <- fread(lst.file[i], header = TRUE)
}

lst <- do.call(rbind, lst)

write.table(lst,outfile, sep = "\t", row.names=F, quote = FALSE)
