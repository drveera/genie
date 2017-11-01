snpfreq = gsmr_data$freq             # minor allele frequency of SNPs
bzx = gsmr_data$bzx     # effects of instruments on risk factor
bzx_se = gsmr_data$bzx_se       # standard errors of bzx
bzx_n = gsmr_data$bzx_n          # sample size for GWAS of the risk factor
std_zx = std_effect(snpfreq, bzx, bzx_se, bzx_n)    # perform standardize
gsmr_data$std_bzx = std_zx$b    # standardized bzx
gsmr_data$std_bzx_se = std_zx$se    # standardized bzx_se
head(gsmr_data)

bzx = gsmr_data$std_bzx     # SNP effects on risk factor 
bzx_se = gsmr_data$std_bzx_se       # standard errors of bzx
bzx_pval = gsmr_data$bzx_pval    # p-values for bzx
bzy = gsmr_data$bzy     # SNP effects on disease
bzy_se = gsmr_data$bzy_se       # standard errors of bzy
gwas_thresh = 5e-8    # GWAS threshold to select SNPs as the instruments for the GSMR analysis
heidi_thresh = 0.01    # HEIDI-outlier threshold
filtered_index = heidi_outlier(bzx, bzx_se, bzx_pval, bzy, bzy_se, ldrho, snp_coeff_id, gwas_thresh, heidi_thresh) # perform HEIDI-outlier analysis
filtered_gsmr_data = gsmr_data[filtered_index,]   # select data passed HEIDI-outlier filtering
filtered_snp_id = snp_coeff_id[filtered_index]   # select SNPs that passed HEIDI-outlier filtering
dim(gsmr_data)

bzx = filtered_gsmr_data$std_bzx    # SNP effects on risk factor
bzx_se = filtered_gsmr_data$std_bzx_se    # standard errors of bzx
bzx_pval = filtered_gsmr_data$bzx_pval   # p-values for bzx
bzy = filtered_gsmr_data$bzy    # SNP effects on disease
bzy_se = filtered_gsmr_data$bzy_se    # standard errors of bzy
filtered_ldrho = ldrho[filtered_gsmr_data$SNP,filtered_gsmr_data$SNP]  # LD correlation matrix of SNPs
gsmr_results = gsmr(bzx, bzx_se, bzx_pval, bzy, bzy_se, filtered_ldrho, filtered_snp_id)    # GSMR analysis 
cat("Effect of exposure on outcome: ",gsmr_results$bxy)

cat("Standard error of bxy: ",gsmr_results$bxy_se)

cat("Standard error of bxy: ",gsmr_results$bxy_se)

cat("Used index to GSMR analysis: ", gsmr_results$used_index[1:5], "...")


