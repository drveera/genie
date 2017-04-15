#!/bin/env Rscript

args <- commandArgs(trailingOnly = TRUE)
phenofile <- args[1]
outname <- args[2]
## since its copied from pheno script, the variable is called pheno
library(data.table)
pheno <- fread(phenofile,header = FALSE)
if(any(grepl("fid",unlist(pheno[1,]), ignore.case = TRUE))){
    names(pheno) <- unlist(pheno[1,])
    names(pheno)[1:2] <- c("fid","iid")
    pheno <- pheno[-1]
} else {
    names(pheno) <- c("fid","iid",paste0("C",1:(ncol(pheno)-2)))
}
pheno$fid <- gsub("^c.*\\*","",pheno$fid)
pheno$fid <- paste(pheno$fid,pheno$iid,sep = "_")
pheno$iid <- pheno$fid
pheno$fatid <- 0
pheno$matid <- 0
pheno$sex <- 0
n = ncol(pheno)
pheno <- pheno[,c(1,2,n-2,n-1,n,3:(n-3)),with=FALSE]
write.table(pheno, outname, sep = "\t", row.names = FALSE, quote = FALSE)

