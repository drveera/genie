# (c) 2016-2021 Huwenbo Shi


import numpy as np, numpy.linalg
import math, sys, io, gzip

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
    compute the ld matrix
arguments:
    1. mat (np.matrix) - the genotype matrix, one snp per row
return:
    1. the ld matrix
"""
def get_ld(mat):
    ld = np.corrcoef(mat)
    ld = np.nan_to_num(ld)
    return np.matrix(ld)


"""
description:
    perform eigenvalue decomposition on the symmetric ld matrix
arguments:
    1. ld (np.matrix) - the ld matrix
return:
    1. eigenvaleus of the ld matrix, sorted from largest to smallest
    2. corresponding eigenvectors of the eigenvalues
"""
def eig_decomp(ld):
    ld_w,ld_v = np.linalg.eigh(ld)
    idx = ld_w.argsort()[::-1]
    ld_w = ld_w[idx]
    ld_v = ld_v[:,idx]
    ld_w = np.matrix(ld_w).transpose()
    ld_v = np.matrix(ld_v)
    return (ld_w, ld_v)


"""
description:
    extract all snps with summary data in the locus
arguments:
    1. snp_beta (dict) - dictionary mapping snp id with beta
    2. snp_beta_info (list) - a lsit of (snp id, pos, n)
    3. locus (tuple) - a tuple of (start pos, end pos)
    3. start_idx (int) - starting index in all_snp at which to extract snps
return:
    1. a list of snp ids for snps in the locus
    2. a list of beta's
    3. index of the last snp in the locus in the list of all snps
"""
def extract_locus_snp(snp_beta, snp_beta_info, locus, start_idx):
    locus_snp = []
    locus_beta = []
    end_idx = start_idx
    for i in range(start_idx, len(snp_beta_info)):
        snp = snp_beta_info[i]
        pos = int(snp[1])
        if(pos >= locus[0] and pos <= locus[1]):
            locus_snp.append(snp)
            locus_beta.append(snp_beta[snp[0]])
        if(pos > locus[1]): break
        end_idx += 1
    return (locus_snp, locus_beta, end_idx)


"""
description:
    find which lines in the reference panel need to be loaded
argument:
    1. snp_idx (dict) - a dictionary mapping snp id with line number in
       reference panel file
    2. locus_snp (list) - a list of snp id's in a locus
return:
    1. a set of lines to load
"""
def get_load_line_idx(snp_idx, locus_snp):
    load_line_idx = set()
    for snp in locus_snp:
        if(snp[0] in snp_idx):
            load_line_idx.add(snp_idx[snp[0]])
    return load_line_idx


"""
description:
    output eigenvalue decomposition and projection squared for each locus
"""
def output_eig_prjsq(chrom, refpanel_snp_idx, refpanel_leg, snp_beta,
    snp_beta_info, part, ref_file, out_file):
    # open files to read and write
    out_file_info = out_file+'_chr'+chrom+'.info.gz'
    out_file_proj = out_file+'_chr'+chrom+'.prjsq.gz'
    out_file_eig = out_file+'_chr'+chrom+'.eig.gz'
    out_file_info = gzip.open(out_file_info, 'wb')
    out_file_proj = gzip.open(out_file_proj, 'wb')
    out_file_eig = gzip.open(out_file_eig, 'wb')
    ref_file = gzip.open(ref_file)
    
    # iterate through locus
    line_idx = 0
    start_idx = 0
    for locus in part:

        # extract snps and beta at a locus
        locus_snp,locus_beta,end_idx = extract_locus_snp(snp_beta,
                        snp_beta_info, locus, start_idx)
        start_idx = end_idx

        # load reference panel for the locus
        load_line_idx = get_load_line_idx(refpanel_snp_idx, locus_snp)
        gens,line_idx = load_reference_panel(ref_file, locus_snp,
            load_line_idx, refpanel_leg, line_idx)

        # check if reference genotypes are loaded correctly
        if(len(locus_beta) != gens.shape[0]):
            sys.stderr.write("An error occurred while loading"
                             " reference panel. Aborting.\n")
            sys.exit(1)

        # check for empty locus
        if(len(locus_beta) == 0):

            out_file_info.write(bytes('%d\t%d\t%d\t%d\t%.1f\n' % (locus[0], locus[1], 0, 0, 0.0), 'utf-8'))
            out_file_eig.write(bytes('%.8f\n' % (0.0), 'utf-8'))
            out_file_proj.write(bytes('%.8f\n' % (0.0), 'utf-8'))
            continue
        
        # compute window ld and its decomposition
        locus_ld = get_ld(gens)
        locus_ld_rank = np.linalg.matrix_rank(locus_ld)
        ld_w,ld_v = eig_decomp(locus_ld)

        # write window info
        locus_n = [elem[2] for elem in locus_snp]
        locus_info = '%d\t%d\t%d\t%d\t%.1f\n' % (locus[0], locus[1],
            gens.shape[0], locus_ld_rank, np.mean(np.array(locus_n)))
        out_file_info.write(bytes(locus_info, 'utf-8'))

        # write eigen values and squared projection
        locus_eig = ''
        locus_proj = ''
        for i in range(locus_ld_rank):
            locus_eig += '%.8f\t' % (ld_w[i,0])
            beta_vec = np.matrix(locus_beta).T
            eig_vec = np.matrix(np.real(ld_v[:,i]))
            locus_proj += '%.8f\t' % (((beta_vec.T*eig_vec)[0,0])**2.0)
        out_file_eig.write(bytes(locus_eig+'\n', 'utf-8'))
        out_file_proj.write(bytes(locus_proj+'\n', 'utf-8'))

    # close files
    ref_file.close()
    out_file_info.close()
    out_file_eig.close()
    out_file_proj.close()
