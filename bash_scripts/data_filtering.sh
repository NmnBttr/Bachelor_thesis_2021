#!/bin/bash
## Filtering steps for southern african dataset using the terminal software tool PLINK (v.1.9):
# 1. Removing individuals that have ambiguas sex according to their genomes
plink --bfile africa_and_refpop --remove africa_and_refpop.nosex --make-bed --out africa_and_refpop_0sexRem

# 2. Remove Duplicates from fam file 
grep "duplicate" africa_and_refpop_0sexRem.fam > duplicate.txt
plink --bfile africa_and_refpop_0sexRem --remove duplicate.txt --make-bed --out africa_and_refpop_0sexRem_dupRem
	
# 3. Remove SNPs and individuals with more than 10% missingness (genotype: --mind 0.1) + include only SNPs with a 90% genotyping rate (--geno 0.1 -> 10% missing)
plink --bfile africa_and_refpop_0sexRem_dupRem --make-bed --mind 0.1 --geno 0.1 --out africa_and_refpop_0sexRem_dupRem_MindGeno

# 4. Prune final data set for LD
plink --bfile africa_and_refpop_0sexRem_dupRem_MindGeno --indep-pairwise 200 25 0.4 --out africa_and_refpop_0sexRem_dupRem_MindGeno_IndPw
plink --bfile africa_and_refpop_0sexRem_dupRem_MindGeno --extract africa_and_refpop_0sexRem_dupRem_MindGeno_IndPw.prune.in --recode12 --make-bed --out africa_and_refpop_0sexRem_dupRem_MindGeno_IndPw_pruned

# 5. Exclude individual with het.haploid genotypes present (Warning 1 from log file)
# Warning: 211 het. haploid genotypes present (see africa_and_refpop_0sexRem_dupRem_MindGeno_IndPw_pruned.hh ); many commands qtreat these as missing.
plink --bfile africa_and_refpop_0sexRem_dupRem_MindGeno_IndPw_pruned --remove africa_and_refpop_0sexRem.hh --make-bed --out africa_and_refpop_0sexRem_dupRem_MindGeno_IndPw_pruned_REMOVEDIND 
	
# 6. Excluding Y chr and MtDNA (Warning 2 from log file)
# Warning: Nonmissing nonmale Y chromosome genotype(s) present; many commands treat these as missing.q
plink --bfile africa_and_refpop_0sexRem_dupRem_MindGeno_IndPw_pruned_REMOVEDIND --not-chr y,mt --make-bed --out africa_and_refpop_0sexRem_dupRem_MindGeno_IndPw_pruned_REMOVEDIND_YMTRem
