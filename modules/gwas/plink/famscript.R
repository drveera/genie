#!/bin/env Rscript

args <- commandArgs(trailingOnly = TRUE)

pheno.file <- args[1]
geno.file <- args[2]
outfile <- args[3]

fam.file <- gsub(".gz$",".fam",pheno.file)
library(data.table)

fam <- fread(fam.file, header=FALSE)
names(fam)[1:2] <- c("FID","IID")
                                        #reading pheno
pheno <- fread(pheno.file, header = TRUE,nrows = 10)
if(grepl("FID",names(pheno))){
  pheno <- fread(pheno.file,header=TRUE)
  names(pheno)[3] <- "pheno"
} else {
  pheno <- fread(pheno.file, header = FALSE)
  names(pheno)[1:3] <- c("FID","IID","pheno")
}
if (!"2" %in% names(table(pheno$pheno))){
  pheno$pheno <- ifelse(pheno$pheno == 1, 2, 1)
}
                                        #----------------
fampheno <- merge(fam,pheno,by=c("FID","IID"), sort = FALSE, all.x = TRUE)
fampheno <- fampheno[,c("FID","IID","V3","V4","V5","pheno")]
fwrite(fampheno,outfile,sep="\t",na="NA")
