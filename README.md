[![Build Status](https://travis-ci.org/drveera/genie.svg?branch=master)](https://travis-ci.org/drveera/genie)
# genie
GEnomic Integrated suitE

## INSTRUCTIONS FOR GENOME.DK USERS
### Installation

#### first download and install latest Miniconda package (don't source from /com/extra/Anaconda..)

```
wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
sh Miniconda3-latest-Linux-x86_64.sh
```
Just accept the defaults 

after installing miniconda,

open a new window and type `conda --version` and see if you have version > 4.0

then install genie by downloading the installer script 

```
wget https://raw.githubusercontent.com/drveera/genie/master/library/ipsych_installer.sh
sh ipsych_installer.sh
```
open a new window and type 
```
source activate genie
```

and you'll be good to go. Type `genie -h` and you'll see help message like this.

```
genie

usage:
 genie <command> [<args>...]

The following commands are available:
COMMAND   DESCRIPTION
gwas      run gwas
geneset   run gene/geneset analysis using gwas summary file
rohs      run analysis of runs of homozygosity
prs       run polygenic risk score analysis
gcta      run GCTA analyses

See 'genie <command> --help' for more information on a specific command.
For example, type 'genie geneset --help'

```


