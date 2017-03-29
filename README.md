[![Build Status](https://travis-ci.org/drveera/genie.svg?branch=master)](https://travis-ci.org/drveera/genie)
# genie
GEnomic Integrated suitE
### Installation

#### source the latest Anaconda package 
```
source /com/extra/Anaconda-Python/LATEST/load.sh
```

#### Check proxy setting
Make sure you have proper proxy settinggs. To check type,`echo $https_proxy` and you should see this value, `http://in:3128`. If its empty, then add this line to your `.bashrc`

```
echo "export https_proxy='http://in:3128'" >> ~/.bashrc
source ~/.bashrc
```
#### Create conda environment 
then create a conda environment with name genie (or whatever u like). 

```
conda create -n genie python=3.6 docopt=0.6.2 
```
#### Install snakemake 
then activate genie and install snakemake, 

```
source activate genie 
pip install --cert /com/etc/ssl-proxy-cert.pem snakemake==3.11.2
```

#### source genie scripts 

```
echo "alias genie='/project/IGdata/faststorage/userdata/iveera/pipelines/genie/genie.py' >> ~/.bashrc
```

