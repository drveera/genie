```
usage:
 genie rare [options] (--vcf=FILE|--bfile=PLINKFILE) (--pheno=FILE|--fam=FILE)
 
options:
 --vcf=FILE                  vcf file
 --bfile=PLINKFILE           plink file without extenstion
 --pheno=FILE                plink pheno file in 2+n column(fid/iid/p1,p2..) format
 --fam=FILE                  plink fam file,  5+n column(fid,iid,motherid,fatherid,sex,p1,p2..) format
                             you can provide only either pheno or fam, not both.
 --pheno-name=NAME           name of the pheno column to analyze
                             applicable to both --pheno and --fam arguments
 --covar=FILE                covariate file (refer to rvtest doc
                             which tests covar is applicable))
 --covar-name=NAMES          comma seperated list of col names in covar file to adjust
 -q                          if phenotype is quantitative
 --single=NAMES              comma seperated list of tests
                             if all, write '--single=all'
                             available-binary-tests:score,wald,exact,dominantExact,firth
                             available-q-tests:score,wald,famLRT,famscore,famGrammerGamma

 --burden=NAMES              comma seperated list of burden tests
                             if all, write '--burden=all'
                             available-binary-tests:cmc,zeggini,mb,fp,exactCMC,cmcWald,rarecover,cmat
                             available-q-tests:cmc,zeggini,cmcWald,famcmc,famzeggini

 --vt=NAMES                  comma seperated list of variable thresholds
                             if all, write '--vt=all'
                             available-binary-thresholds:price
                             available-q-thresholds:price,analytic

 --kernel=NAMES             comma seperated list of kernel models
                            if all, write '--kernel=all'
                            available-binary-kernels:skat,skato
                            available-q-kernels:skat,skato,kbac,famSkat

 --meta=NAMES               comma seperated list of meta names
                            if all, write '--meta=all'
                            available-binary-tests:score,dominant,recessive,cov
                            available-q-tests:score,dominant,recessive,cov

 --raremetal                If meta analysis of results from multiple vcf files are desired
 --geneFile=RANGE           in refFlat format
 --gene=GENENAMES           comma seperated list of GENE ids
 --out=PREFIX               outname prefix [default: rare_out]
 --nojob                    front end
 --njobs=NUMBER             number of parallel jobs if running in front end
 --dry-run                  dry run
```
