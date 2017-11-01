import pandas as pd
import sys
sys.path.insert(1, sys.path[0] + '/../../../library')
import loglib

f1, f2, clumped, g1k, out = sys.argv[1:]
logger = loglib.get_logger(out)

logger.info(f"reading {f1}")
df1 = pd.read_csv(f1, sep='\s+')
logger.info(f"{len(df1)} snps read\n")
df_clumped = pd.read_csv(clumped, sep='\s+')
df1 = df1[df1.SNP.isin(df_clumped.SNP)]
logger.info(f"{len(df1)} snps from {f1} in clumped\n")

logger.info(f"reading {f2}")
df2 = pd.read_csv(f2, sep='\s+')
logger.info(f"{len(df2)} snps read\n")
df1 = df1.rename(columns={'A1': 'a1', 'A2': 'a2', 'FRQ': 'freq', 'OR': 'bzx', 'SE': 'bzx_se', 'N': 'bzx_n', 'P': 'bzx_pval'})
df2 = df2.rename(columns={'A1': 'a1', 'A2': 'a2', 'FRQ': 'freqy', 'OR': 'bzy', 'SE': 'bzy_se', 'N': 'bzy_n', 'P': 'bzy_pval'})
df = pd.merge(df1, df2, on=['CHR', 'POS', 'a1', 'a2'])
logger.info(f"{f1} and {f2} merged. {len(df)} snps.\n")

logger.info(f"reading {g1k}")
g1kf = pd.read_csv(g1k, sep='\s+', header=None, names=['CHR', 'SNP', 'GPOS','POS', 'A1', 'A2'])
logger.info(f"{len(g1kf)} snps read\n")

m = pd.merge(df, g1kf, left_on='SNP_x', right_on='SNP')
mis = m[~(((m.A1 == m.a1) | (m.A1 == m.a2)) & ((m.A2 == m.a1) | (m.A2 == m.a2)))]

df = df[~df.SNP_x.isin(mis.SNP)]
logger.info(f"removed snps with mismatched alleles. {len(df)} snps remaining\n")
df = df.drop(['CHR', 'POS', 'SNP_y', 'freqy'], axis=1)
df = df.rename(columns={'SNP_x': 'SNP'})

logger.info(f"Writing snps to {out}.sumstats and {out}.allele")
df.to_csv(f"{out}.sumstats", sep='\t', index=False)
df[['SNP', 'a1', 'a2']].to_csv(f"{out}.allele", sep='\t', index=False)

