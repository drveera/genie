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

if (! file.info(paste0(pfix,".annovar.avinput2"))$size == 0){
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
##f1
f1 <-  merge(anno1, avinput1, by = c("Chr","Start","End","Ref","Alt"))
f1 <- f1[,c("SNP","avsnp147"), with = FALSE]

##f2
if (! is.null(avinput2)){
    f2 <- merge(anno2, avinput2, by = c("Chr","Start","End","Ref","Alt"))
    f2 <- f2[,c("SNP","avsnp147")]
}


## merge with summary
m1 <- merge(sumstat, f1, by = "SNP", all.x = TRUE, sort = FALSE)
if (! is.null(avinput2)){
    m1 <- merge(m1, f2, by = "SNP", all.x = TRUE, sort = FALSE)
}


## function
updateids <- function(x,y){
    if (is.na(x)){
        return(y)
    } else {
        return(x)
    }
}

m1$SNP <- apply(m1,1, function(x) updateids(x[20],x[1]))
m1 <- m1[,1:19,with=FALSE]
write.table(m1,outname, sep = "\t", row.names = FALSE, quote = FALSE)


