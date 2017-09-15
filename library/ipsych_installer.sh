#!/bin/sh


export https_proxy='http://in:3128'
#source /com/extra/Anaconda-Python/LATEST/load.sh
echo "ssl_verify: /com/etc/ssl-proxy-cert.pem" > ~/.condarc
conda create -n genie python=3.6 docopt=0.6.2
source activate genie
pip install --cert /com/etc/ssl-proxy-cert.pem snakemake==4.0.0
echo "alias genie='/project/IGdata/faststorage/userdata/iveera/pipelines/genie/genie.py'" >> ~/.bashrc
source ~/.bashrc
echo "done!"
