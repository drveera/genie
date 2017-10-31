# (c) 2016-2021 Huwenbo Shi


import sys, math, os, gzip
import numpy as np

"""
description:
    load legend file for reference panel
arguments:
    1. legend_file_name (str) - path to the legend file
return:
    1. a dictionary that maps snp id with line number
    2. a list of snp ids in the order they appear in the legend
""" 
def load_legend(legend_file_name):
    all_snps = []
    legend_file = gzip.open(legend_file_name, 'rt')
    snp_idx = dict()
    idx = 0
    for line in legend_file:
        cols = line.strip().split()
        snpid = cols[0]
        ref_alt = cols[2]+cols[3]
        all_snps.append((snpid, ref_alt))
        snp_idx[snpid] = idx
        idx += 1
    legend_file.close()
    return (snp_idx, all_snps)


"""
description:
    load effect size (beta) from z-score file
arguments:
    1. zscore_file_name (str) - path to the z-score file
return:
    1. a dictionary that maps snp id with beta
    2. a list of (snp id, position, sample size) in the order they
       appear in the z-score file
"""
def load_beta(zscore_file_name):
    all_snps = []
    snp_beta = dict()
    first_line_read = False
    zscore_file = open(zscore_file_name, 'rt')
    for line in zscore_file:
        if(not first_line_read):
            first_line_read = True
            continue
        cols = line.strip().split()
        pos = int(cols[1])
        ref_alt = cols[2].upper()+cols[3].upper()
        zscore = float(cols[4])
        n = float(cols[5])
        beta = zscore / math.sqrt(n)
        snp_beta[cols[0]] = beta
        all_snps.append((cols[0], pos, n, ref_alt))
    zscore_file.close()
    return (snp_beta, all_snps)


"""
description:
    load partition file
arguments:
    1. partition_file_name (str) - path to the partition file
return:
    1. a list of (start position, end position)
"""
def load_partition(partition_file_name):
    partition = []
    first_line_read = False
    partition_file = open(partition_file_name, 'rt')
    for line in partition_file:
        # skip first line
        if(first_line_read == False):
            first_line_read = True
            continue
        cols = line.strip().split()
        start_pos = int(cols[1])
        end_pos = int(cols[2])-1
        partition.append((start_pos, end_pos))
    partition_file.close()
    return partition


"""
description:
    load specific lines in the reference panel
arguments:
    1. ref_panel_file (file) - file id of the reference panel file
    2. locus_snp (list) - a list of snp ids in desired order
    3. lines_to_load (set) - lines to load in the reference panel file
    4. legend (list) - legend of the reference panel file
    5. start_line (int) - line number at which the loading start
return:
    1. the genotype matrix (one snp per row)
    2. line index at which the loading ends
"""
def load_reference_panel(ref_panel_file, locus_snp, lines_to_load,
                         legend, start_line):
    # load raw data from reference panel
    snp_idx = dict()
    ref_data = []
    end_line = start_line
    num_snp_to_load = len(lines_to_load)
    num_snp_loaded = 0
    idx = 0
    while(num_snp_loaded < num_snp_to_load):
        line = ref_panel_file.readline()
        if(not line): break
        if(end_line in lines_to_load):
            snp = legend[end_line][0]
            cols = line.strip().split()
            ref_data.append(cols)
            snp_idx[snp] = idx
            num_snp_loaded += 1
            idx += 1
        end_line += 1
    ref_data = np.matrix(ref_data).astype(float)
    
    # make sure the order is correct
    gens = np.matrix(np.zeros((len(locus_snp),ref_data.shape[1])))
    for i in range(len(locus_snp)):
        gens[i,:] = ref_data[snp_idx[locus_snp[i][0]],:]
    
    return (gens, end_line)


"""
description:
    load output from step 1
argument:
    1. prefix (str) - prefix of the file names generated in step 1
output:
    1. a list of (chrom, start, end, num_snp, rank, sample size)
    2. a list of np.matrix of eigen values at each loci
    3. a list of np.matrix of projection squares at each loci
"""
def load_step1(prefix):
    
    # load info
    locus_info = []
    for i in range(1,23):
        fnm = '%s_chr%d.info.gz' % (prefix, i)
        if(not os.path.exists(fnm)):
            continue
        fnm = gzip.open(fnm, 'rt')
        for line in fnm:
            line = line.strip()
            cols = line.split()
            locus_info.append((i,cols[0],cols[1],cols[2],cols[3],cols[4]))
        fnm.close()

    # load eigs
    all_eig = []
    for i in range(1,23):
        fnm = '%s_chr%d.eig.gz' % (prefix, i)
        if(not os.path.exists(fnm)):
            continue
        fnm = gzip.open(fnm, 'rt')
        for line in fnm:
            line = line.strip()
            cols = line.split()
            tmp = np.matrix([float(cols[i]) for i in range(len(cols))])
            all_eig.append(tmp)
        fnm.close()

    # load prjsq
    all_prj = []
    for i in range(1,23):
        fnm = '%s_chr%d.prjsq.gz' % (prefix, i)
        if(not os.path.exists(fnm)):
            continue
        fnm = gzip.open(fnm, 'rt')
        for line in fnm:
            line = line.strip()
            cols = line.split()
            tmp = np.matrix([float(cols[i]) for i in range(len(cols))])
            all_prj.append(tmp)
        fnm.close()

    return locus_info,all_eig,all_prj
