import sys
import pandas as pd
import os
from bioinfokit import visuz


def main(argv):
    if len(argv) != 4:
        print("give as input: \n 1st autosome meanQ file \n 2rd x chr meanQ file \n 3th full filename of fam_meta_file.csv")
    else:
        # open input files 
        #aut_path = os.path.join(argv[1], argv[2])
        with open(argv[1]) as meanQ_A_file:
            a_df = pd.read_csv(meanQ_A_file, sep=' ',header=None, dtype='float',engine='python')
        #x_path = os.path.join(argv[3], argv[4])
        with open(argv[2]) as meanQ_X_file:
            x_df = pd.read_csv(meanQ_X_file, sep=' ',header=None, dtype='float',engine='python')
        with open(argv[3]) as f:
            fam_df = pd.read_csv(f, sep=',',usecols=[0,6,9],names=["ID","Continent","Population"]) # make sure separator is the right one
        
        ### prepare files for plotting ###
        a_df = a_df.join(fam_df["ID"])
        x_df = x_df.join(fam_df["ID"])
        
        merged_df = x_df.merge(a_df, how="inner", on="ID") # int_x : X chr columns and int_y : Autosome columns
        merged_df = merged_df.join(fam_df["Population"])
        # set gene names as index
        df = merged_df.set_index(merged_df["Population"])
        df = df.drop('Population', 1)
        df = df.drop('ID', 1)
        df.head(2)

        # heatmap with hierarchical clustering 
        visuz.gene_exp.hmap(df=df, cmap='RdYlGn',dim=(x_df.shape[1]-1,a_df.shape[1]-1), tickfont=(3, 2))


if __name__ == "__main__":  # pragma: nocover
    main(sys.argv)