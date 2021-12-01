################################################################################
#  fastSTRUCTURE for all autosomes at once
#
#
#  fastSTRUCTURE is an algorithm for inferring population structure from large SNP genotype data.
#  https://rajanil.github.io/fastStructure/
#
#
#  INSTRUCTIONS:
#  This snakemake assumes that you have installed fastStructure in conda environment called fastStructure.
#  You should change path to your conda.sh when sourcing.
#  Please copy this Snakemake file to your directory
#  (e.g. directory where is your .bed file) and change only parameters
#  within "PARAMETERS GIVEN TO fastSTRUCTURE".
#  You can specify how many K's and how many runs per K you want to run.
#  "FILENAME" should contain the name of the .bed file on which you want to
#  run ADMIXTURE but without ".bed" at the end
#  (e.g. if your file is called: myfilename.bed then FILENAME ="myfilename").
#  Once you changed parameters you can run the Snakemake
#  from the directory where your .bed file is with the following command
#  (after adjusting --cluster specifications i.e. jobname -J; and path to the data -D):
#
#  snakemake -s fastSTRUCTURE_all_autosomes.Snakefile -j 50 -k --cluster "sbatch -p nowick -J A_fStr -D /data/scratch/bajiv90/admixture_Namuun/hgdp/Autosomes -o %x.%j.out -t 15-00:00:00 -c 12 --mem-per-cpu=15000"
#
#
#  07/07/2021
#  Vladimir Bajic
################################################################################





################################################################################
#### PARAMETERS GIVEN TO fastSTRUCTURE #########################################
################################################################################

#### Specify file name (without ".bed" extension)
##FILENAME = "HGDP_0sexRem_YMTRem_MindGeno_pruned"
FILENAME = "africa_and_refpop_0sexRem_dupRem_MindGeno_IndPw_pruned_REMOVEDIND_YMTRem_autosome"

#### Specify how many runs per each K to run
R = list(range(0,10))
#R = 1
#### Specify number of K's to run
#K = list(range(2, 10))
K = 10
################################################################################
################################################################################
################################################################################


rule all:
    input:
        expand("K{k}_R{r}/{f}_R{r}.{k}.meanQ", f=FILENAME, r=R, k=K)


rule fastSTRUCTURE:
    output:
        "K{k}_R{r}/{f}_R{r}.{k}.meanQ"
    shell:
        """
set +eu;
source /home/namuub98/anaconda3/etc/profile.d/conda.sh;
conda activate fastStructure;
mkdir -p K{wildcards.k}_R{wildcards.r};
structure.py -K {wildcards.k} --input {wildcards.f} --output K{wildcards.k}_R{wildcards.r}/{wildcards.f}_R{wildcards.r}
set -eu;
	"""
