# (c) 2016-2021 Huwenbo Shi


import math, io
import numpy as np, numpy.linalg


eps = 10.0**-8.0         # a small number to avoid division by 0
pct_use_win_gc = 0.5     # per cent of loci used to estimate lambda gc


"""
description:
    get raw/biased local heritability estimates
arguments:
    1. locus_info (list) - a list of (chrom, start, end, num snp, rank, n)
    2. all_eig (list of np.matrix) - eigenvalues of ld matrices at all loci
    3. all_prj (list of np.matrix) - projection squared at all loci
    4. max_k (int) - maximum number of eigenvectors to use
    5. eig_thres (float) - threshold on eigenvalues
    6. gc (None of float) - genomic control factor, lambda gc
return:
    1. a list of (raw estimate, k)
"""
def get_raw_h2g(locus_info, all_eig, all_prj, max_k, eig_thres, gc):
    raw_est = []
    for i in range(len(locus_info)):
        k = min(max_k, np.where(all_eig[i] > eig_thres)[0].size)
        tmp = np.divide(all_prj[i][0,0:k], all_eig[i][0,0:k]+eps)
        raw_est.append((np.sum(tmp)*gc, float(k)))
    return raw_est


"""
description:
    estimate genomic control factor, lambda gc
arguments:
    1. locus_info (list) - a list of (chrom, start, end, num snp, rank, n)
    2. all_eig (list of np.matrix) - eigenvalues of ld matrices at all loci
    3. all_prj (list of np.matrix) - projection squared at all loci
    4. max_k (int) - maximum number of eigenvectors to use
    5. eig_thres (float) - threshold on eigenvalues
return:
    1. estimated lambda gc
"""
def estimate_lambda_gc(locus_info, all_eig, all_prj, num_eig, eig_thres):
    
    # compute biased raw estimate
    raw_est = get_raw_h2g(locus_info, all_eig, all_prj,
                    num_eig, eig_thres, 1.0)

    # compute observed local heritability and theoretical local
    # heritability under the null of no heritability
    obs_th = []
    num_win = len(locus_info)
    for i in range(num_win):
        n = float(locus_info[i][5])
        obs_th.append([raw_est[i][0], raw_est[i][1]/(n+eps)])
    obs_th = np.matrix(sorted(obs_th, key=lambda x: x[0]))

    # assuming top 50% of windows are the null
    m = int(pct_use_win_gc*num_win)
    gc = (np.linalg.pinv(obs_th[0:m,0])*obs_th[0:m,1])[0,0]

    return max(gc, 1.0)


"""
description:
    estimate local heritability jointly, when total h2g is unknown
arguments:
    1. locus_info (list) - a list of (chrom, start, end, num snp, rank, n)
    2. all_eig (list of np.matrix) - eigenvalues of ld matrices at all loci
    3. all_prj (list of np.matrix) - projection squared at all loci
    4. num_eig (int) - maximum number of eigenvectors to use
    5. eig_thres (float) - threshold on eigenvalues
    6. sens_thres (float) - sensitivity threshold
    7. gc (float) - genomic control factor, lambda gc
return:
    1. an np.matrix of unbiased local heritability estimates
    2. a list of (raw_est, k)
    3. estimated/specified lambda gc
    4. total number of snps
"""
def get_local_h2g_joint(locus_info, all_eig, all_prj, num_eig,
    eig_thres, sense_thres, gc):
    
    # estimate gc if not provided
    if(gc is None):
        gc = estimate_lambda_gc(locus_info, all_eig, all_prj,
                num_eig, eig_thres)
    
    # choose max k
    num_win = len(locus_info)
    num_snp = np.sum([float(elem[3]) for elem in locus_info])
    tot_n = np.sum([float(elem[5])*float(elem[3]) for elem in locus_info])
    avg_n = tot_n/num_snp
    max_k = (sense_thres*avg_n-avg_n)/(sense_thres*num_win+eps)
    max_k = min(int(math.ceil(max_k)), num_eig)

    # adjust for bias
    raw_est = get_raw_h2g(locus_info, all_eig, all_prj, max_k, eig_thres, gc)
    A = np.matrix(np.zeros((num_win, num_win)))
    b = np.matrix(np.zeros((num_win, 1)))
    for i in range(num_win):
        n = float(locus_info[i][5])
        for j in range(num_win):
            if(i == j):
                A[i,j] = n-raw_est[i][1]
            else:
                A[i,j] = -raw_est[i][1]
        b[i,0] = n*raw_est[i][0]-raw_est[i][1]
    est = np.linalg.pinv(A)*b
    
    return est,raw_est,gc,num_snp


"""
description:
    compute variance estimates when local heritability
    is estimated jointly
arguments:
    1. locus_info (list) - a list of (chrom, start, end, num snp, rank, n)
    2. all_h2g (np.matrix) - a matrix of local heritability
return:
    1. a np.matrix of estimated variance
"""
def get_var_est_joint(locus_info, all_h2g):
    num_win = len(locus_info)
    tot = np.sum(all_h2g)
    A = np.matrix(np.zeros((num_win, num_win)))
    b = np.matrix(np.zeros((num_win, 1)))
    for i in range(num_win):
        n = float(locus_info[i][5])
        p = float(locus_info[i][4])
        for j in range(num_win):
            if(i == j):
                A[i,j] = 1.0
            else:
                A[i,j] = p/(n-p+eps)
                A[i,j] = -A[i,j]*A[i,j]
        b[i,0] = ((n/(n-p+eps))**2.0)
        b[i,0] *= (2.0*p*((1.0-tot)/(n+eps))+4.0*all_h2g[i,0])
        b[i,0] *= ((1.0-tot)/(n+eps))
    var_est = np.linalg.pinv(A)*b
    return var_est


"""
description:
    estimate local heritability independently, given total snp heritability
arguments:
    1. locus_info (list) - a list of (chrom, start, end, num snp, rank, n)
    2. all_eig (list of np.matrix) - eigenvalues of ld matrices at all loci
    3. all_prj (list of np.matrix) - projection squared at all loci
    4. num_eig (int) - maximum number of eigenvectors to use
    5. eig_thres (float) - threshold on eigenvalues
    6. gc (None of float) - genomic control factor, lambda gc
    7. tot_h2g (float) - total snp heritability
return:
    1. an np.matrix of unbiased local heritability estimates
    2. a list of (raw_est, k)
    3. estimated/specified lambda gc
    4. total number of snps
"""
def get_local_h2g_indep(locus_info, all_eig, all_prj, num_eig,
        eig_thres, sense_thres, gc, tot_h2g):
    
    # estimate gc if not provided
    if(gc is None):
        gc = estimate_lambda_gc(locus_info, all_eig, all_prj,
                num_eig, eig_thres)

    # choose max k
    num_win = len(locus_info)
    avg_n = np.mean(np.array([float(elem[5]) for elem in locus_info]))
    max_k = (sense_thres*avg_n)/(num_win+eps)
    max_k = min(int(math.ceil(max_k)), num_eig)

    # adjust for bias
    num_snp = 0
    raw_est = get_raw_h2g(locus_info, all_eig, all_prj, max_k, eig_thres, gc)
    est = np.matrix(np.zeros((num_win,1)))
    for i in range(num_win):
        est[i,0] = raw_est[i][0]
        est[i,0] -= (1.0-tot_h2g)*raw_est[i][1]/(float(locus_info[i][5])+eps)
        num_snp += int(locus_info[i][3])
    return est,raw_est,gc,num_snp


"""
description:
    compute variance estimates when local heritability
    is estimated independently
arguments:
    1. locus_info (list) - a list of (chrom, start, end, num snp, rank, n)
    2. all_h2g (np.matrix) - a matrix of local heritability
    3. tot_h2g_se (float) - standard error of total snp heritability
return:
    1. a np.matrix of estimated variance
"""
def get_var_est_indep(locus_info, all_h2g, tot_h2g_se):
    num_win = len(locus_info)
    var_est = np.matrix(np.zeros((num_win,1)))
    for i in range(num_win):
        h2g = all_h2g[i,0]
        n = float(locus_info[i][5])
        p = float(locus_info[i][4])
        var = 1.0
        var = var*((n/(n-p+eps))**2)
        var = var*(2*p*((1-h2g)/(n+eps))+4*h2g)
        var = var*((1-h2g)/(n+eps))
        var_est[i,0] = var+(tot_h2g_se*p/(n+eps))**2.0
    return var_est


"""
description:
    output local h2g estimates
arguments:
    1. out_file (str) - file name for output file
    2. locus_info (list) - a list of (chrom, start, end, num snp, rank, n)
    3. raw_est (list) - a list of (raw_h2g, k)
    4. all_h2g (np.matrix) - a matrix of local heritability estimates
    5. all_var (np.matrix) - variance estimates for all_h2g
return:
    nothing
"""
def output_local_h2g(out_file, locus_info, raw_est, all_h2g, all_var):
    out_file = open(out_file, 'w')
    out_file.write('chr\tstart\tend\tnum_snp\tk\tlocal_h2g\tvar\n')
    num_win = len(locus_info)
    for i in range(num_win):
        line = '%s\t%s\t%s\t%s\t%d\t%.10f\t%.12f' % (
            locus_info[i][0], locus_info[i][1], locus_info[i][2],
            locus_info[i][3], raw_est[i][1], all_h2g[i,0], all_var[i,0])
        out_file.write(line+'\n')
    out_file.close()
