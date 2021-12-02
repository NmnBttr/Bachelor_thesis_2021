import sys
import pandas as pd
import os
import numpy as np

def check_elem(max_elem_index, check_col,maxs,row):
    ### match the columns of two files, so there are no duplications A_1~X_2 and A_4~
    if len(maxs)==row.shape[0]:
        return check_col,maxs
    elif max_elem_index not in check_col:  
        check_col.append(max_elem_index)
        maxs.append(row[max_elem_index])
        return check_col,maxs
    else:
        new_row = np.sort(row)[::-1]
        for i in range(1,new_row.shape[0],1):
            new_max_index = np.where(row == new_row[i])
            if new_max_index not in check_col:
                return check_elem(new_max_index[0][0],check_col,maxs,row) 

def calc_corr(a_df,x_df): 
    res = np.zeros(shape=(int(a_df.shape[1]), int(x_df.shape[1])), dtype=float) # init
    corr = np.corrcoef(a_df,x_df,rowvar=False) # calculating column-wise Pearson product-moment correlation matrix
    k = int(corr.shape[0]/2)
    # print(corr)
    for i in range(int(a_df.shape[1])):
        for j in range(int(x_df.shape[1])):
            res[i][j] = corr[k+i][j] # getting the values from upper right corner of corr matrix
    
    check_col = []
    maxs = []

    if np.isnan(res).any() == True:
        ### if file contains empty K return empty result
        check_col = [0]
        maxs = [0]
        return check_col, maxs 
    else:
        ### getting max corr from the correlation matrix ###
        for row in res:
            max_elem = np.nanargmax(row) # np.nanmax(row)
            result = check_elem(max_elem,check_col,maxs,row)
    return result

def compare_files(file1_path, file2_path):

    res_max = np.zeros(shape=(10, 10), dtype=float) # 10 because we have 10 runs
    res_min = np.zeros(shape=(10, 10), dtype=float)
    col_filenames1 = [] # for autosome file names 
    col_filenames2 = [] # for x chr file names

    ### reading autosome files ###
    for i,filename1 in enumerate(os.listdir(file1_path)):
        if filename1.endswith(".meanQ"): # reading only meanQ files in path/directory
            with open(file1_path+"/"+filename1) as meanQ_file1:  
                a_df = np.genfromtxt(meanQ_file1,delimiter=' ',dtype='<f8') # array = row in file 
                #print(a_df)
                file_id1='Aut_'+filename1[-10:-8]+'_K'+filename1[-7:-6]
                col_filenames1.append(file_id1) # Autosome file names
                ### reading x chr files ###
                for j,filename2 in enumerate(os.listdir(file2_path)):
                    if filename2.endswith(".meanQ"): # reading only meanQ files in path/directory
                        with open(file2_path+"/"+filename2) as meanQ_file2:
                            x_df = np.genfromtxt(meanQ_file2,delimiter=' ')
                            #print(x_df)
                            cor_res = calc_corr(a_df,x_df)
                            #print(cor_res)
                            res_max[i][j] = np.nanmax(cor_res[1])
                            res_min[i][j] = np.nanmin(cor_res[1])
                            file_id2='Xchr_'+filename2[-10:-8]+'_K'+filename2[-7:-6]
                            col_filenames2.append(file_id2)
                    else:
                        print("Mean Q X chromosome files do not exist in directory")
                        exit
        else:
            print("Mean Q Autosome files do not exist in directory")
            exit

    col_filenames2 = col_filenames2[:10] # X chr file names 
    ### getting highest max corrs from max corr matrix ###
    maxs = np.nanmax(res_max)
    #print(res_max)
    max_index_col = np.unravel_index(np.argmax(res_max), res_max.shape) #tuple index (autosome,xchr)
    print("Best maximal correlation: "+str(maxs)+' between '+col_filenames1[max_index_col[0]],col_filenames2[max_index_col[1]])

    ### getting highest min corr from min corr matrix ###
    min_corr = np.nanmax(res_min) # max corr from each row of res_max
    #print(res_min)
    mins = np.nanmin(min_corr)
    min_index_col = np.where(res_min == mins) # get index of min value (autosome,xchr)
    print("Best minimal correlation: "+str(mins)+' between '+col_filenames1[int(min_index_col[0])],col_filenames2[int(min_index_col[1])])

    ### save min and max correlation between all autosomal and all x chr files as a csv file ###
    # corr_table_max = pd.DataFrame()
    # corr_table_max['Autosomes_vs_Xchr'] = col_filenames1
    # for i,elem in enumerate(col_filenames2):
    #     corr_table_max[elem]=res_max[:,i]
    # print(corr_table_max)
    # #corr_table_max.to_csv("max_corr_table_A_B_AC_vs_X_B_K3_test.csv",sep=',')
    
    # corr_table_min = pd.DataFrame()
    # corr_table_min['Autosomes_vs_Xchr'] = col_filenames1
    # for j,val in enumerate(col_filenames2):
    #     corr_table_min[val]=res_min[:,j]
    # print(corr_table_min)
    #corr_table_min.to_csv("min_corr_table_A_B_AC_vs_X_B_K3_test.csv",sep=',')
    return 


def main(argv):
    ### Reading files ###
    if len(argv)!= 3:
        print("Input1: path to directory with autosomes meanQ files;\nInput2: path to directory with X chr meanQ files;")
        return
    else:
        if (os.path.exists(argv[1]) & os.path.exists(argv[2])):
            path_to_autosomes = argv[1]
            path_to_xchr = argv[2]
            ### Calculating minimal and maximal correlation between autosome and x chr files ###
            compare_files(path_to_autosomes,path_to_xchr)
        else: 
            print("Paths does not exist or\n Please check if the datasets are comparable with each other!")
    return

if __name__ == "__main__":  # pragma: nocover
    main(sys.argv)