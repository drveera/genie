#!/bin/env Rscript

args <- commandArgs(trailingOnly = TRUE)

anno1 <- args[1]
outname <- args[2]

library(data.table)
if (! file.info(anno1)$size == 0){
    anno1 <- fread(anno1, header = TRUE, colClasses = "character")
    avinput2 <- anno1[is.na(avsnp147)]
    avinput2$End <- as.numeric(as.character(avinput2$Start)) + (nchar(avinput2$Alt)-1)
    avinput2 <- avinput2[,c(1,2,3,5,4,6),with=FALSE]
    write.table(avinput2, outname, col.names = FALSE, row.names = FALSE, quote = FALSE, sep = "\t")
} else {
    a = "Nothing left to annotate"
    write.table(a,outname)
}

