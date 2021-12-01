#!/bin/bash
# Splitting data set into Autosomes and X chromosomes using the software PLINK (v.1.9):
#	- Separate dataset into Autosomes and X chr
#	- Separate datasets into females and males only for both Autosomes and X chr
#	  -> follow the steps from Ancestry package html	 
#	1. everything from autosomes (just split and run)
#	2. randomly choose equal number of snps from autosomes and x chr (look at files how many snps we have)
#	3. split each autosomes into separate chr and run for each of them estimates
#		- incase chr have much more than x chr we downsize the sample
#		- each chr separately compared to x chr
#		- splitting and subsampling -> look at admixture papers for the idea
##############################################################################################
# 1) Separate dataset into Autosomes and X chromosome
# dividing it into autosomes and X chromosome	
plink --bfile africa_and_refpop_0sexRem_dupRem_MindGeno_IndPw_pruned_REMOVEDIND_YMTRem --autosome --out Autosomes/africa_and_refpop_0sexRem_dupRem_MindGeno_IndPw_pruned_REMOVEDIND_YMTRem_autosome --make-bed

# Number of SNPs in: i) Xchr = 3120; ii) Autosome = 338587
plink --bfile africa_and_refpop_0sexRem_dupRem_MindGeno_IndPw_pruned_REMOVEDIND_YMTRem --chr 1 --out Xchr/africa_and_refpop_0sexRem_dupRem_MindGeno_IndPw_pruned_REMOVEDIND_YMTRem_Xchr --make-bed

#2) Splitiing Autosomes into separate chrommosomes
plink --bfile africa_and_refpop_0sexRem_dupRem_MindGeno_IndPw_pruned_REMOVEDIND_YMTRem_autosome --chr 1 --out chr1/africa_and_refpop_0sexRem_dupRem_MindGeno_IndPw_pruned_REMOVEDIND_YMTRem_chr1 --make-bed
# Number of SNPs i.e.:	chr1 = 28341;	chr2 = 29156;	chr3 = 24031;	chr4 = 20858;	chr5 = 21162

#3) Splitting into females and males
cd /mnt/genotyping/Vladimir/ancestryPackage/africa
mkdir Autosomes/femalesOnly
mkdir Autosomes/malesOnly
mkdir Xchr/femalesOnly
mkdir Xchr/malesOnly

plink --bfile africa_and_refpop_0sexRem_dupRem_MindGeno_IndPw_pruned_REMOVEDIND_YMTRem_autosome --filter-males --out africa_and_refpop_0sexRem_dupRem_MindGeno_IndPw_pruned_REMOVEDIND_YMTRem_autosome_malesOnly --make-bed

plink --bfile africa_and_refpop_0sexRem_dupRem_MindGeno_IndPw_pruned_REMOVEDIND_YMTRem_autosome --filter-females --out africa_and_refpop_0sexRem_dupRem_MindGeno_IndPw_pruned_REMOVEDIND_YMTRem_autosome_femalesOnly --make-bed

plink --bfile africa_and_refpop_0sexRem_dupRem_MindGeno_IndPw_pruned_REMOVEDIND_YMTRem_Xchr --filter-males --out africa_and_refpop_0sexRem_dupRem_MindGeno_IndPw_pruned_REMOVEDIND_YMTRem_Xchr_malesOnly --make-bed

plink --bfile africa_and_refpop_0sexRem_dupRem_MindGeno_IndPw_pruned_REMOVEDIND_YMTRem_Xchr --filter-females --out africa_and_refpop_0sexRem_dupRem_MindGeno_IndPw_pruned_REMOVEDIND_YMTRem_Xchr_femalesOnly --make-bed

# 4) Get number of SNPs
plink --bfile africa_and_refpop_0sexRem_dupRem_MindGeno_IndPw_pruned_REMOVEDIND_YMTRem_chr1 --write-snplist
	
# 5) Filtering females and males per chromosome
for i in {1..22}; do
	cd chr$i
	mkdir malesOnly
	mkdir femalesOnly
	plink --bfile africa_and_refpop_0sexRem_dupRem_MindGeno_IndPw_pruned_REMOVEDIND_YMTRem_chr$i --filter-males --out /nfs/group/ag_nowick/data/ancestry_packages/admixture_Namuun/africa/Autosomes/chr$i/malesOnly/africa_and_refpop_0sexRem_dupRem_MindGeno_IndPw_pruned_REMOVEDIND_YMTRem_malesOnly_chr$i --make-bed
	plink --bfile africa_and_refpop_0sexRem_dupRem_MindGeno_IndPw_pruned_REMOVEDIND_YMTRem_chr$i --filter-females --out /nfs/group/ag_nowick/data/ancestry_packages/admixture_Namuun/africa/Autosomes/chr$i/femalesOnly/africa_and_refpop_0sexRem_dupRem_MindGeno_IndPw_pruned_REMOVEDIND_YMTRem_femalesOnly_chr$i --make-bed
	cd ..
done
