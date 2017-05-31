#!/bin/env Rscript

args <- commandArgs(trailingOnly = TRUE)

library(ggman)
library(data.table)

sumstat.file <- args[1]
plot.file <- args[2]

sumstat <- fread(sumstat.file,header = TRUE)

p1 <- ggman(sumstat, pvalue = "P1df", size = 1)
p1
ggsave(plot.file)
