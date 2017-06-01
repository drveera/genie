#!/bin/env Rscript

args <- commandArgs(trailingOnly = TRUE)

geno.file <- args[1]
pheno.file <- args[2]
covar.file <- args[3]
outfile.pheno <- args[4]
outfile.summary <- args[5]

require(GenABEL)
require(data.table)
                                        #retrieve the ids from gbl.out
idfile <- paste0(outfile.pheno,".ids.txt")
system(paste0("sed -n 2p ", geno.file, " > ",idfile))
ids <- readLines(idfile)
ids <- unlist(strsplit(ids,split = " "))

                                        #prepare the pheno file
pheno <- fread(pheno.file,header=TRUE)
trait <- names(pheno)[3]
if ("2" %in% names(table(pheno[,3]))){
  p <- pheno[,3]
  p <- ifelse(p == 2, 1, 0)
  pheno[,3] <- p
}
covar <- fread(covar.file, header = TRUE)
covars <- names(covar)[3:ncol(covar)]
dfm <- merge(pheno,covar,by=c("FID","IID"))
names(dfm) <- gsub("IID","id",names(dfm))
ids <- data.frame(id = ids)
dfm <- merge(ids,dfm,by = "id",all.x=TRUE)
dfm$sex <- rep(1,nrow(dfm))
##remove files
system(paste0("rm ",idfile))
write.table(dfm,outfile.pheno,row.names=FALSE,sep="\t")
##run association
cat("Loading geno data \n" )
geno <- load.gwaa.data(phenofile = outfile.pheno,genofile = geno.file,force = TRUE)
cat("Running association analysis \n")
f <- as.formula(paste0(trait,"~",paste(covars,collapse = "+")))
#f <- as.formula(paste0(trait,"~1"))
print(f)

##rslt <- mlreg(f, data = geno, trait.type = "guess")
rslt <- qtscore(f, data = geno, trait.type = "binomial")

cat("done \n")
rslt <- results(rslt)
rslt$SNP <- row.names(rslt)
rslt <- data.table(rslt)
cat("writing the results \n")
fwrite(rslt,outfile.summary,sep="\t",na  = "NA")

