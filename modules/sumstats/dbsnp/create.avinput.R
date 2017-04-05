args <- commandArgs(trailingOnly = TRUE)
sumstatfile = args[1]
pfix = args[2]


library(data.table)
if (grepl("gz$",sumstatfile)){
    sumstat = fread(paste0("zcat ", sumstatfile), header = TRUE, colClasses = "character")
}else {
    sumstat = fread(sumstatfile, header = TRUE, colClasses = "character")
}
##functions
mywrite = function(x,y){
    write.table(x,y,row.names=F, col.names = F,quote = F, sep = "\t")
}
##subset
withids <- sumstat[grep("^rs",SNP)]
mywrite(withids,paste0(pfix,".withids"))

withoutids <- sumstat[!grep("^rs",SNP)]
mywrite(withoutids,paste0(pfix,".withoutids1"))

withoutids$BP2 <- as.numeric(as.character(withoutids$BP)) + (nchar(withoutids$A1) -1)
avinput <- withoutids[,c("CHR","BP","BP2","A1","A2","SNP"),with = FALSE]
mywrite(avinput,paste0(pfix,".annovar.avinput1"))
