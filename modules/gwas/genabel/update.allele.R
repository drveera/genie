#!/bin/env Rscript

args <- commandArgs(trailingOnly = TRUE)

rslt <- args[1]
outfile <- args[3]

map <- gsub(".gbl",".map",rslt)
library(data.table)

rslt <- fread(rslt)
map <- fread(map)

map <- map[,c(2,4,5,6),with = FALSE]
names(map) <- c("SNP","Position","a1","a2")

dfm <- merge(rslt,map,by=c("SNP","Position"))
fwrite(dfm,outfile,sep="\t",na="NA")

