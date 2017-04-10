#!/bin/env Rscript

args <-  commandArgs(trailingOnly = TRUE)

cat(args[1],",",args[2],",",args[3],"\n")
sumstatfile <- args[1]
pfix <- args[2]
outname <- args[3]

library(data.table)
## read files
anno1 <- fread(paste0(pfix,".anno1.hg19_multianno.txt"), header = TRUE, colClasses = "character")
if (!file.info(paste0(pfix,".anno2.hg19_multianno.txt"))$size == 0){
    anno2 <- fread(paste0(pfix,".anno2.hg19_multianno.txt"), header = TRUE, colClasses = "character")
} else {
    anno2 <- NULL
}

avinput1 <- fread(paste0(pfix,".annovar.avinput1"), header = FALSE, colClasses = "character")
names(avinput1) <- c("Chr","Start","End","Ref","Alt","SNP")

if (! nrow(anno2) == 0){
    avinput2 <- fread(paste0(pfix,".annovar.avinput2"), header = FALSE, colClasses = "character")
    names(avinput2) <- c("Chr","Start","End","Ref","Alt","SNP")
} else {
    avinput2 <- NULL
}

if (grepl("gz$",sumstatfile)){
    sumstat = fread(paste0("zcat ", sumstatfile), header = TRUE, colClasses = "character")
}else {
    sumstat = fread(sumstatfile, header = TRUE, colClasses = "character")
}

##merge 
##f1
library(plyr)
avinput1$sno <- 1:nrow(avinput1)
f1 <- join(avinput1, anno1)
##f1 <-  merge(anno1, avinput1, by = c("Chr","Start","End","Ref","Alt"))
f1 <- f1[!duplicated(sno)]
f1 <- f1[,c("SNP","avsnp147"), with = FALSE]

##f2
if (! is.null(avinput2)){
    avinput2$sno <- 1:nrow(avinput2)
    f2 <- join(avinput2, anno2)
    f2 <- f2[!duplicated(sno)]
    ##f2 <- merge(anno2, avinput2, by = c("Chr","Start","End","Ref","Alt"))
    f2 <- f2[,c("SNP","avsnp147")]
}


## merge with summary
##m1 <- merge(sumstat, f1, by = "SNP", all.x = TRUE, sort = FALSE)
sumstat$sno2 <- 1:nrow(sumstat)
m1 <- join(sumstat,f1)
m1 <- m1[!duplicated(sno2)]
if (! is.null(avinput2)){
    f2$sno3 <- 1:nrow(f2)
    m2 <- join(m1,f2)
    print("done")
    m2 <- m2[!duplicated(sno2)]
    ##m1 <- merge(m1, f2, by = "SNP", all.x = TRUE, sort = FALSE)
    m1 <- m2
    m1 <- m1[order(sno2),]
}


## function
updateids <- function(x,y){
    if (is.na(x)){
        return(y)
    } else {
        return(x)
    }
}
idpos <- grep("avsnp147",names(m1))
snppos <- grep("SNP",names(m1))
m1$SNP <- apply(m1,1, function(x) updateids(x[as.numeric(idpos)],x[as.numeric(snppos)]))
#m1 <- m1[,1:19,with=FALSE]
write.table(m1,outname, sep = "\t", row.names = FALSE, quote = FALSE)
