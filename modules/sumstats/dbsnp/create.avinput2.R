#!/bin/env Rscript

args <- commandArgs(trailingOnly = TRUE)

anno1 <- args[1]
outname <- args[2]

library(data.table)
system("echo something left to annotate >> av2file")
anno1 <- fread(anno1, header = TRUE, colClasses = "character")
avinput2 <- anno1[is.na(avsnp147)]
avinput2$End <- as.numeric(as.character(avinput2$Start)) + (nchar(avinput2$Alt)-1)
avinput2 <- avinput2[,c(1,2,3,5,4,6),with=FALSE]
write.table(avinput2, outname, col.names = FALSE, row.names = FALSE, quote = FALSE, sep = "\t")

if (file.info(outname)$size == 0){
    writeLines("Nothing left to annotate", outname)
}

