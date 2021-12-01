#!/bin/bash
# Running fastSTRUCTURE using Snakemake:

snakemake -s fastSTRUCTURE_autosomes.Snakefile -j 5 -k --cluster "sbatch -p big -J A_B_PC_fStr -D /data/scratch/namuub98/admixture/africa/A_B_PC -o %x.%j.out -t 15-00:00:00 -c 1 --mem-per-cpu=15000"

# 1. get a table of empty K's for each folder (from Baja):

for k in {2..9}; do for r in {0..9}; do echo "K "${k}" R "${r}" EmptyKs"; awk '{for (i=1;i<=NF;i++) sum[i]+=$i} END{for (i in sum) printf "%d%s", sum[i], (i==NF?"\n":" ")}' K${k}_R${r}/*Q | grep -o ' 0' | wc -l ; done; done | paste - 

# 2. get emptyKs>0: 

awk '{ if ($6 > 0) { print } }' emptyKs.txt

# 3. get optimal K with "chooseK.py" from fastSTRUCTURE:

chooseK.py --input=K?_R?/africa_and_ref_pop_0sexRem_YMTRem_MindGeno_pruned_Xchr*
