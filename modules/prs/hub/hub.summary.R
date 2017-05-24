#!/bin/env Rscript

args <- commandArgs(trailingOnly = TRUE)

sumfiles <- args[1]
outname <- args[2]

sumfiles <- readLines(sumfiles)

library(data.table)
library(ggplot2)
library(gtools)


sumlist <- list()
for(i in 1:length(sumfiles)){
    sumlist[[i]] <- fread(sumfiles[i], header = TRUE)    
}
sumdfm <- do.call(rbind, sumlist)
thold <- sumdfm$threshold
thold <- thold[!duplicated(thold)]
sumdfm$threshold <- factor(sumdfm$threshold, levels = thold[mixedorder(thold)])
sumpheno <- sumdfm[pheno == basename(outname)]
p1 <- ggplot(sumdfm,aes(threshold,R2, group = pheno)) + geom_line(alpha = 0.1) +
    theme(axis.text.x=element_text(angle=90, hjust=1)) +
    labs(x = "P Value Thresholds", y = "Nagelkerke-R-Squared", title = paste0(basename(outname),"r2.plot")) +
    geom_line(data = sumpheno, aes(colour = pheno)) +
    scale_x_discrete(labels = c("S1" = "<5e-8","S2" = "<1e-6","S3" = "<1e-4","S4" = "<0.001","S5" = "<0.01","S6" = "0.05","S7" = "0.1","S8" = "0.2",
                                "S9" = "0.5","S10" = "1")) +
    theme(axis.text.x = element_text(angle = 90, hjust = 1))

ggsave(paste0(outname,"rsquaredValues.allpheno.pdf"), width = 8, height = 4)

plotslist <- readRDS(paste0(outname,"plots.RDS"))
plotslist[[length(plotslist)+1]] <- p1

pdf(paste0(outname,"summary.pdf"))
for (i in 1:length(plotslist)){
    print(plotslist[[i]])
}
dev.off()
                         
