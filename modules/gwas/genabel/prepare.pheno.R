#!/bin/env Rscript

args <- commandArgs(trailingOnly = TRUE)

geno.file <- args[1]
pheno.file <- args[2]
covar.file <- args[3]
outfile <- args[4]

require(GenABEL)
require(data.table)
                                        #retrieve the ids from gbl.out
idfile <- paste0(outfile,".ids.txt")
system(paste0("sed -n 2p ", geno.file, " > ",idfile))
ids <- readLines(idfile)
ids <- unlist(strsplit(ids,split = " "))

                                        #prepare the pheno file
pheno <- fread(pheno.file,header=TRUE)
if ("2" %in% names(table(pheno[,3]))){
  p <- pheno[,3]
  p <- ifelse(p == 2, 1, 0)
  pheno[,3] <- p
}
covar <- fread(covar.file, header = TRUE)
dfm <- merge(pheno,covar,by=c("FID","IID"))
names(dfm) <- gsub("IID","id",names(dfm))
ids <- data.frame(id = ids)
dfm <- merge(ids,dfm,by = "id",all.x=TRUE)
##remove files
system(paste0("rm ",idfile))
write.table(dfm,outfile,row.names=FALSE,sep="\t")


