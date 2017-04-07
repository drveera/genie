#!/bin/env Rscript

args <- commandArgs(trailingOnly=TRUE)

if (is.na(args[3])){
    stop("inadequate number of arguments")
}

dfmfilelist <- args[1]
outpdf <- args[2]
facetting <- as.logical(args[3])
dfmfiles <- readLines(dfmfilelist)
dfmlist <- list()
for(i in 1:length(dfmfiles)){
    d  <- read.table(dfmfiles[i], header = TRUE)
    if (nrow(d)>0){
        tname <- gsub(".pos.*$","",basename(dfmfiles[i]))
        tname <- gsub("^.*-","",tname)
        d$tname <- tname
        dfmlist[[i]] <- d   
    }
}
dfm <- do.call(rbind, dfmlist)

library(ggplot2)
if (! is.null(dfm)){
    p1 <- ggplot(dfm, aes(x = ID, y = tname)) +
        geom_tile(aes(fill = -log10(TWAS.P))) +
        theme(axis.text.x = element_text(angle = 90, hjust = 1), text = element_text(size=10)) +
        scale_fill_gradient(low = "white", high = "red")
    if (facetting){
        p1 <- p1 + facet_grid(MODEL~.,drop=T,space="free",scales="free")
    }
    p1
}
ggsave(outpdf, width = 20, height = 8)





