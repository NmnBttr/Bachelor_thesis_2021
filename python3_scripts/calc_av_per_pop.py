import sys
import pandas as pd
import numpy as np

## this script is for calculating the average difference per population 

def merge_files(diff_file, fam_file):
    with open(fam_file) as f:
        meta_colm = pd.read_csv(f, sep=',',usecols=[6,9,7],header=None)
    with open(diff_file) as d:
        df_file = pd.read_csv(d,sep='\t')
        df_file['Population'] = meta_colm.iloc[:,2] # adding population column to delta admix df
        df_file['Continent'] = meta_colm.iloc[:,0]
        df_file['Country'] = meta_colm.iloc[:,1]
    return df_file

def calc_average(df):
    ### split df into african and non-african ###
    av_table = pd.DataFrame()
    av_table['Population'] = df['Population'].unique()
    N_col = []
    s = (len(df['Population'].unique()),len(df.columns)-3)
    mean_col=np.zeros(s,dtype=float)
    col_names = []
    for c in enumerate(df['Population'].unique()):
        temp_df = df[df['Population'] == c[1]]
        N_col.append(len(temp_df)) # number of individuals
        for j in range(len(df.columns)-3):
            col_names.append("col_"+str(j))
            mean = temp_df.iloc[:,j].mean()
            mean_col[c[0],j] = round(mean,2)        
    col_names = col_names[:mean_col.shape[1]]
    av_table['N'] = N_col
    for i, elem in enumerate(col_names):
        av_table[elem]=pd.Series(mean_col[:,i])
    return av_table

def main(argv):
    if len(argv)!= 4:
        print("Input1: diff file;\nInput2: fam files;\nInput3: outputname for average_per_pop_file.csv")
        return
    else:
        diff_file = argv[1]
        fam_file = argv[2]
        df = merge_files(diff_file,fam_file)
        
        av = calc_average(df)
        name = argv[3]
        av.to_csv(name,sep='\t')
        print("File "+name+" has been computed.")
    return

if __name__ == "__main__":  # pragma: nocover
    main(sys.argv)