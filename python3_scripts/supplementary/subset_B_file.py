import sys
import pandas as pd
import numpy as np

## this script is for calculating the average difference per population 

def merge_files(diff_file, fam_file):
    with open(fam_file) as f:
        meta_colm = pd.read_csv(f, sep='\t',usecols=[0],header=None)
    with open(diff_file) as d:
        df_file = pd.read_csv(d,sep=' ')
        df_file['ID'] = meta_colm.iloc[:,0]
    return df_file

def main(argv):
    if len(argv)!= 4:
        print("Input1: diff_B_file;\nInput2: fam files;\nInput3: fam file for only one sex")
        return
    else:
        diff_file = argv[1]
        fam_file = argv[2]
        fam_one_file = argv[3]
        df = merge_files(diff_file,fam_file)
        ID_colm = pd.DataFrame()

        with open(fam_file) as f:
            IDs = pd.read_csv(fam_one_file, sep=',',usecols=[0],header=None)
            ID_colm["ID"] = IDs.iloc[:,0]

        subset = df.merge(ID_colm, how="inner", on="ID")
        subset.drop(subset.columns[subset.shape[1]-1],axis=1,inplace=True) ## removing ID column
        fc = fam_one_file.count("femalesOnly")
        mc = fam_one_file.count("malesOnly")
        if (fc==1 & mc==1):
            subset.to_csv("B_file_Xchr_femalesOnly_subset_R0.3.meanQ",index=False,sep=' ')
            print("B_file_femalesOnly_subset_RX.3.meanQ is now created")
        else:
            subset.to_csv("B_file_malesOnly_subset.meanQ",index=False,sep=' ')
            print("B_file_malesOnly_subset.csv is now created") 
    return

if __name__ == "__main__":  # pragma: nocover
    main(sys.argv)