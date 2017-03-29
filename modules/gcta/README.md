
To install genie in iPSYCH cluster, follow the instruction in the main page (here). 

If you have followed the instruction in the main page, by now you will have your own conda environment to activate. So first activate the environment by, 

```
source /com/extra/Anaconda-Python/LATEST/load.sh
source activate genie
```

So now, if you type `genie -h `, you will see the main help message. 

Now type, `genie gcta -h`, to see all the submodules under gcta module. To know the options for any of the submodules, for example bivariate, type `genie gcta bivariate -h`. 

The help message should self explanatory.  Here is the preview of the help message, 

```
usage:
 gcta variance --grm=GRMFILE --pheno=FILE [options]

options:
 --pheno=FILE          plink format pheno file
 --mpheno=NUMBER       if multiple phenotypes in pheno file, specify which one to use
 --grm=GRMFILE         grm file
 --out=PREFIX          outname prefix [default: variance_out]
 --keep=FILE           list file
 --reml-priors=N1      two numbers
 --reml-alg=NUMBER     0(AI) or 1(AI) or 2(EM)
 --reml-no-constrain   allow negative
 --reml-maxit=NUMBER   maximum number of iterations
 --gxe                 test gxe
 --covar=FILE          covariate file
 --qcovar=FILE         quantitative covariate file
 --reml-lrt=NUMBER     see GCTA doc
 --reml-no-lrt         turn off the LRT
 --prevalence=NUMBER   prevalence of the disease
 --dry-run             show only the code
 --nojob               front end

description:
The arguments here are exactly the same arguments used in GCTA software.
To know how to use these arguments, please see the GCTA web page (http://cnsgenomics.com/software/gcta/reml.html).
A typical example submission command for a case-control trait would be like,
    genie gcta variance --grm=test --pheno test.phen --prevalence 0.01 --out test_null

```
