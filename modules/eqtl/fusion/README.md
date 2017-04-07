## FUSION

### Installation

Follow the main page of genie for instalation. After installing genie, activate it.

```
source activate genie
```

then type, 

```
genie eqtl fusion -h

```

You'll see the following help message. 

```
usage:
 eqtl fusion [options] --sumstats=FILE

options:
 --sumstats=FILE       summary statistics file or .list
 --weights=FILE        gene expression weights file or .list [default: |resources/fusion/weights.list]
 --chr=NUMBER          chromosome number
 --out=PREFIX          output prefix [default: genie_fusion]
 --nojob               nojob
 --dry-run             dry run

```

Example run, 

```
genie eqtl fusion --sumstats=summary.txt --out=run1
```


