import sys
import pandas as pd
from pylab import *
from enum import unique
import seaborn as sns
import matplotlib.pyplot as plt 

def get_corr(diff1,diff2):
    res1=[]
    col_names1 = []
    col_names2 = []
    for col1 in diff1.columns:
        for col2 in diff2.columns:
            res1.append(diff1[col1].astype('float32').corr(diff2[col2].astype('float32')))
            col_names1.append("B_subset_"+col1)
            col_names2.append("F_"+col2)
    #print(res1,col_names1)
    corr =pd.DataFrame()
    corr["B_subset_col"] = col_names1
    corr["F_col"] = col_names2
    corr["corr"] = res1
    return corr


def main(argv):
    if len(argv)!= 5:
        print("Input1: diff file B subset;\nInput2: diff file for one sex;\nInput3: fam_file_for_one_sex;")# \n Input4: outputname for plot name")
        return
    else:
        num_ind = pd.DataFrame()
        with open(argv[3]) as f:
            pop_colm = pd.read_csv(f, sep=',',usecols=[9],header=None)
        with open(argv[1]) as diff_file_B:
            diff1 = pd.read_csv(diff_file_B, sep='\t',header=0)       
        with open(argv[2]) as diff_file_F:
            diff2 = pd.read_csv(diff_file_F, sep='\t',header=0)
        with open(argv[4]) as av_diff_file_F: # get number of individuals per pop
            av_diff2 = pd.read_csv(av_diff_file_F, sep=',',skiprows=0)
            num_ind = av_diff2.iloc[:,1]
            #print(num_ind)
        corr = get_corr(diff1,diff2)
        diff1["Population"]=pop_colm.iloc[:,0]
        diff2["Population"]=pop_colm.iloc[:,0]

        column_names_B = ["diff_of_0_and_0", "diff_of_1_and_2","diff_of_2_and_1"]
        column_names_F = ["diff_of_1_and_1","diff_of_0_and_2","diff_of_2_and_0","Population"] #ordered for matching columns to B file columns
        #column_names_M = ["diff_of_1_and_0","diff_of_0_and_2","diff_of_2_and_1","Population"]
        diff2 = diff2.reindex(columns=column_names_F)
        #diff2 = diff2.reindex(columns=column_names_M)
        
        result = pd.DataFrame(index=[diff1["Population"].unique(),num_ind]) 

        cor_col0=[]
        cor_col1=[]
        cor_col2=[]
        for k,pop in enumerate(diff2['Population'].unique()):
            temp_df1 = diff1.loc[diff1['Population']== pop]
            temp_df2 = diff2.loc[diff2['Population']== pop]

            cor_col0.append(temp_df1[column_names_B[0]].astype('float32').corr(temp_df2[column_names_F[0]].astype('float32')))
            cor_col1.append(temp_df1[column_names_B[1]].astype('float32').corr(temp_df2[column_names_F[1]].astype('float32')))
            cor_col2.append(temp_df1[column_names_B[2]].astype('float32').corr(temp_df2[column_names_F[2]].astype('float32')))
            # cor_col0.append(temp_df1[column_names_B[0]].astype('float32').corr(temp_df2[column_names_M[0]].astype('float32')))
            # cor_col1.append(temp_df1[column_names_B[1]].astype('float32').corr(temp_df2[column_names_M[1]].astype('float32')))
            # cor_col2.append(temp_df1[column_names_B[2]].astype('float32').corr(temp_df2[column_names_M[2]].astype('float32')))
        result["corr_A_pop1"]=cor_col0
        result["corr_A_pop2"]=cor_col1
        result["corr_A_pop3"]=cor_col2

        ## Plotting heatmap 
        sns.set_context("paper", font_scale=0.5)
        sns.heatmap(result, cmap ='RdYlGn',linewidths=1).set(ylabel="Population-Number of individuals")
        #plt.show() #annot=True,
        #plt.savefig("corr_between_B_subsetF_and_F_per_pop", dpi=1200)
        result = result.reindex(columns=["Population","N","corr_A_pop1","corr_A_pop2","corr_A_pop3"])
        #result.to_csv("corr_between_B_subsetF_and_F_per_pop.csv",sep='\t',na_rep='NA')
        #result.to_csv("corr_between_B_subsetM_and_M_per_pop.csv",sep='\t',na_rep='NA')
    return
        
if __name__ == "__main__":  # pragma: nocover
    main(sys.argv)