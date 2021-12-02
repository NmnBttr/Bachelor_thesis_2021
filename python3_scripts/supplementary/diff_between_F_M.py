import sys
import pandas as pd
from pylab import *

def get_corr(diff1,diff2):
    # for calculating correlation between the columns of two given dataframe 
    diff1 = diff1.drop(columns=['Population'])
    diff2 = diff2.drop(columns=['Population'])
    diff1 = diff1.drop(columns=['N_F'])
    diff2 = diff2.drop(columns=['M_N'])
    res1=[]
    col_names1 = []
    col_names2 = []
    for col1 in diff1.columns:
        for col2 in diff2.columns:
            res1.append(diff1[col1].astype('float32').corr(diff2[col2].astype('float32')))
            col_names1.append(col1)
            col_names2.append(col2)

    corr =pd.DataFrame()
    corr["F_col"] = col_names1
    corr["M_col"] = col_names2
    corr["corr"] = res1
    return corr

def main(argv):
    if len(argv)!= 4:
        print("Input1: average diff filename F;\n Input2: average diff filename M;,\n Input3: average diff filename B; \n")# Input4: outputname for plot name")
        return
    else:
        with open(argv[1]) as av_diff_file_F:
            av_diff1 = pd.read_csv(av_diff_file_F, sep=',',header=0)
        with open(argv[2]) as av_diff_file_M:
            av_diff2 = pd.read_csv(av_diff_file_M, sep=',',header=0)
            print(av_diff2)
        with open(argv[3]) as av_diff_file_B:
            av_diff3 = pd.read_csv(av_diff_file_B, sep=',',header=0)
        
        #c = get_corr(av_diff1,av_diff3)
        #print(c)
        
        # for joining all 3 datasets into one by common entries
        column_names_M = ["Population","M_N","M_col_0", "M_col_2", "M_col_1"]
        av_diff2 = av_diff2.reindex(columns=column_names_M)
        m_av = av_diff1.merge(av_diff2, how="inner", on="Population")
        column_names_B = ["Population","B_N","B_col_0", "B_col_2", "B_col_1"]
        av_diff3 = av_diff3.reindex(columns=column_names_B)

        # building final dataframe with diff of F-M and sum 
        sum_df = pd.DataFrame()
        sum_df["Population"]=m_av["Population"]
        sum_df["diff_popA"] = round(m_av["F_col_0"]-m_av["M_col_0"],2)
        sum_df["diff_popB"] = round(m_av["F_col_1"]-m_av["M_col_2"],2)
        sum_df["diff_popC"] = round(m_av["F_col_2"]-m_av["M_col_1"],2)
        sum_df["sum_A_pops"] = round(sum_df["diff_popA"]+sum_df["diff_popB"]+sum_df["diff_popC"],2)
        
        sum_df = m_av.merge(sum_df,how="inner", on="Population")
        sum_df = sum_df.merge(av_diff3,how="inner", on="Population")

        # saving dataframe as a csv file
        sum_df.to_csv("sum_of_diff_between_F_M_and_B.csv",sep='\t',na_rep='NA')
    return

if __name__ == "__main__":  # pragma: nocover
    main(sys.argv)