#!/bin/bash
#Visiualise fastStructure output with PONG v1.4.9:

# creating PONG filemap:

for i in $(ls K*R*/*Q); do echo -e ${i%/*}'\t'${i%_Run*/*}'\t'$(pwd)'/'$i; done | awk '{print $1 "\t" substr($2,2,1) "\t" $3; }' > pong_filemap

# creating pong_pop_order:

cut -f 7,12 fam_with_meta_HGDP_0sexRem_YMTRem_MindGeno_pruned.txt | uniq > pong_pop_order
sort pong_pop_order | uniq
sort -u -k 1 pong_pop_order > pong_pop_order_sorted
tac pong_pop_order_sorted > pong_pop_order2
awk '{print $2}' pong_pop_order2 > pong_pop_ordered

# Running PONG:

pong -m pong_filemap -n pong_pop_ordered -i pong_ind2pop
