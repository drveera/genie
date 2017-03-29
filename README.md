[![Build Status](https://travis-ci.org/drveera/genie.svg?branch=master)](https://travis-ci.org/drveera/genie)
# genie
GEnomic Integrated suitE
### Installation

*You need to do this only once*

Download this script and run it
```
wget https://raw.githubusercontent.com/drveera/genie/master/library/ipsych_installer.sh
sh ipsych_installer.sh
```
Once you run this script, then everytime when u want to run genie, you should activate the genie environment by

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
For example, type 'ipsych geneset --help'

```


