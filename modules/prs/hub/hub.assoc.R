#!/bin/env Rscript

args <- commandArgs(trailingOnly = TRUE)
scorefile <- args[1]
phenofile <- args[2]
covarfile <- args[3]
outname <- args[4]
plotslist <- list()

if (is.na(args[3])){
    stop("inadequate arguments")
}

##imports
library(data.table)
library(plyr)
library(fmsb)
library(ggplot2)
library(ggrepel)
library(tidyverse)
library(gtools)

##reads
prs <- fread(scorefile,header=TRUE)
names(prs)[1:2] <- c("IID","FID")
ts <- names(prs)[3:ncol(prs)]

pheno <- fread(phenofile)
names(pheno)[1:3] = c("IID","FID","pheno1")

##recode pheno
if ("2" %in% names(table(pheno$pheno1))){
    pheno$pheno1 <- with(pheno, replace(pheno1,pheno1==1,0))
    pheno$pheno1 <- with(pheno, replace(pheno1,pheno1==2,1))
}

covar <- fread(covarfile)
names(covar)[1:2] = c("IID","FID")
covariables <- names(covar)[3:ncol(covar)]

##merge 
m1 <- join(pheno,covar, type = "inner")
if(nrow(m1) == 0){
    stop("Mismatch of IDs between pheno and covar files")
}
m2 <- join(prs,m1, type = "inner")
if(nrow(m2) == 0){
    stop("mismatch of IDs between pheno/covar and score filese")
}


dfmlist <- list()
for (i in 1:length(ts)){
    f <- as.formula(paste0("pheno1~",ts[i],"+",paste(covariables,collapse = "+")))
    res <- glm(f, data = m2, family = "binomial")
    r2 <- NagelkerkeR2(res)
    res <- summary(res)$coefficients
    threshold <- rownames(res)[2]
    res <- res[2,]
    res <- c(res,r2,threshold)
    dfmlist[[i]] <- res
}

dfm <- do.call(rbind,dfmlist)
dfm <- as.data.frame(dfm)
names(dfm) <- c("Estimate","SE","Z_score","pvalue","N","R2","threshold")
dfm$R2 <- as.numeric(dfm$R2)
dfm$threshold <- as.character(dfm$threshold)
dfm$pvalue <- as.numeric(as.character(dfm$pvalue))
dfm <- dfm[mixedorder(dfm$threshold),]
fwrite(dfm,paste0(outname,"results.txt"),sep = "\t", na = "NA")
dfm_best <- dfm[dfm$R2 == max(dfm$R2),]

##plot r squared
p1 <- ggplot(dfm, aes(threshold,as.numeric(R2))) + geom_point() + geom_line(aes(group = 1),alpha = 0.1) +
    geom_point(data = dfm_best, colour = "red") +
    geom_text_repel(aes(label = format(pvalue,scientific = TRUE)), size = 2) +
    geom_text(data = dfm_best,
                    aes(y = 0, label = paste0("best_threshold:",threshold)), colour = "blue") +
    theme(axis.text.x=element_text(angle=90, hjust=1)) +
    labs(x = "P Value Thresholds", y = "Nagelkerke-R-Squared", title = paste0(basename(outname),"r2.plot"))
plotslist[[1]] <- p1
ggsave(paste0(outname,"rsquaredValues.pdf"))

## determine the best fit score
best_threshold <- as.character(dfm[dfm$R2 == max(dfm$R2),"threshold"])
m2$bestscore <- m2[,names(m2) %in% best_threshold,with=F]
m2 = m2 %>%
    mutate(quantile = ntile(bestscore,10))
m2$quantile <- as.factor(m2$quantile)
qs <- model.matrix(~quantile, data = m2)
print(head(qs))
qs <- as.data.frame(qs)
m2 <- cbind(m2,qs)
m2$quantile <- ifelse(m2$quantile == 1,"base","other")

qspecor <- function(dfm,qtile){
    dfm$qtile <- dfm[,qtile]
    dfm <- with(dfm, dfm[quantile == "base" | qtile == 1,])
    f <- as.formula(paste0("pheno1~quantile+",paste(covariables, collapse = "+")))
    mdl <- glm(f, data = dfm)
    or <- exp(coef(mdl)[2])
    ci <- exp(confint(mdl))[2,]
    return(c(or,ci,qname=qtile))
}

orlist <- list()
qtiles <- paste0("quantile",2:10)
print(names(m2))
for(i in 1:length(qtiles)){
    orlist[[i]] <- qspecor(m2,qtiles[i])
}
ordfm <- do.call(rbind,orlist)
ordfm <- rbind(c("1","1","1","quantile1"),ordfm)
ordfm <- as.data.frame(ordfm)


ordfm[,1] <- as.numeric(as.character(ordfm[,1]))
ordfm[,2] <- as.numeric(as.character(ordfm[,2]))
ordfm[,3] <- as.numeric(as.character(ordfm[,3]))
names(ordfm) <- c("or","lower","upper","quantile")
ordfm$quantile <- factor(ordfm$quantile, levels = paste0("quantile",1:10))

p2 <- ggplot(ordfm, aes(quantile,or)) + geom_point() +
    geom_errorbar(aes(ymax = upper, ymin = lower), width = 0.2) +
    labs(x = "Quantiles", y = "Odds ratio with 95% CI", title = paste0(basename(outname),".or.plot"))
plotslist[[2]] <- p2
ggsave(paste0(outname, "oddsratio_decile.pdf"))

pdf(paste0(outname,"summary.pdf"))
for (i in 1:length(plotslist)){
    print(plotslist[[i]])
}
dev.off()
