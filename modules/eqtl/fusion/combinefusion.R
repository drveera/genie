#!/bin/env Rscript

args <- commandArgs(trailingOnly = TRUE)
if (is.na(args[5])){
    stop("Inadequate arguments")
}

rdir <- args[1]
datout <- args[2]
topout <- args[3]
incout <- args[4]
dropout <- args[5]

datfiles <- list.files(rdir, pattern = "*all$", full.names = TRUE)
write(rdir,"debug.txt", append=TRUE)
datlist <- list()
for (i in 1:length(datfiles)) datlist[[i]] <- read.table(datfiles[i], header = TRUE)
datdfm <- do.call(rbind, datlist)
write.table(datdfm, datout, sep = "\t", row.names = F, quote = F)

topfiles <- list.files(rdir, pattern = "*top$", full.names = TRUE)
toplist <- list()
for (i in 1:length(topfiles)){
    if (!file.info(topfiles[i])$size == 0){
        toplist[[i]] <- read.table(topfiles[i], header = TRUE)
    }
}
topdfm <- do.call(rbind, toplist)
topdfm$FILE <- basename(as.character(topdfm$FILE))
write.table(topdfm, topout, sep = "\t", row.names = F, quote = F)

droppedfiles <- list.files(rdir, pattern = "*dropped.dat$", full.names = TRUE)
droplist <- list()
for (i in 1:length(droppedfiles)) {
    if (!file.info(droppedfiles[i])$size == 0){
        droplist[[i]] <- read.table(droppedfiles[i], header = TRUE)
    }
}
dropdfm <- do.call(rbind, droplist)
dropdfm$FILE <- basename(as.character(dropdfm$FILE))
write.table(dropdfm, dropout, sep = "\t", row.names = F, quote = F)

incfiles <- list.files(rdir, pattern = "*included.dat$", full.names = TRUE)
inclist <- list()
for (i in 1:length(incfiles)) {
    if (!file.info(incfiles[i])$size == 0){
        inclist[[i]] <- read.table(incfiles[i], header = TRUE)
    }
}
incdfm <- do.call(rbind, inclist)
incdfm$FILE <- basename(as.character(incdfm$FILE))
write.table(incdfm, incout, sep = "\t", row.names = F, quote = F)
