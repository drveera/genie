#!/bin/env Rscript

args <- commandArgs(trailingOnly = TRUE)

sumstats.file <- args[1]
clump.file <- args[2]
outfile <- args[3]

library(data.table)

sumstats <- fread(sumstats.file)
sumstats <- sumstats[,-c("P")]
names(sumstats) <- gsub("Z","BETA",names(sumstats))
clump <- read.table(clump.file, header = TRUE)

dfm <- merge(sumstats,clump, by = "SNP")

write.table(dfm,outfile, sep = "\t", row.names=F, quote = F)
