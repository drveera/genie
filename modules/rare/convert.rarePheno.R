#!/bin/env Rscript

args <- commandArgs(trailingOnly = TRUE)
phenofile <- args[1]
outname <- args[2]

library(data.table)
pheno <- fread(phenofile,header = FALSE)
if(any(grepl("fid",unlist(pheno[1,]), ignore.case = TRUE))){
    names(pheno) <- unlist(pheno[1,])
    names(pheno)[1:3] <- c("fid","iid","y1")
    pheno <- pheno[-1]
} else {
    names(pheno) <- c("fid","iid",paste0("y",1:(ncol(pheno)-2)))
}
pheno$fid <- gsub("^c.*\\*","",pheno$fid)
pheno$fid <- paste(pheno$fid,pheno$iid,sep = "_")
pheno$iid <- pheno$fid
pheno$fatid <- 0
pheno$matid <- 0
pheno$sex <- 0
n = ncol(pheno)
pheno <- pheno[,c(1,2,n-2,n-1,n,3:(n-3)),with=FALSE]
if (!2 %in% pheno$y1){
    pheno$y1 <- with(pheno, ifelse(y1 == 1, 2, 1))
}
write.table(pheno, outname, sep = "\t", row.names = FALSE, quote = FALSE)

