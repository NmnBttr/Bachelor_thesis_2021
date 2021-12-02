import csv
from os import path
import pandas as pd

def read_file(filename):
    """
    Reads given files.

    :param infile[0]: meanQ file from Autosomes
    :param infile[1]: meanQ file from X chromosomes
    :rtype: pandas.DataFrame
    """
    try:
        with open(filename, "r") as meanQ_file:
            meanQ_reader = csv.reader(meanQ_file)
            result = []
            for row in meanQ_reader:
                result.append(row[0].split(" "))
            result = pd.DataFrame(result)
        return result
    except Exception as e:
        return "An error has occured at read_file: " + str(e)

def get_corr_col(file1,file2):
    """
    Calculates Pearson correlation between the columns of the two files in order to compare the right columns with eachother.

    :param infile[0]: pandas.DataFrame from Autosomes file
    :param infile[1]: pandas.DataFrame from X chromosomes file
    :rtype: List of pairs
    """
    res = pd.DataFrame()
    c1 =[]
    c2 =[]
    pairs = []
    for col1 in file1.columns:
        for col2 in file2.columns:
            print(col1,col2)
            # print(file1[col1])
            res = file1[col1].astype('float64').corr(file2[col2].astype('float64'))
            print(res)
            if res > 0.9:
                c1.append(col1)
                c2.append(col2)
                pair = (col1,col2)
                pairs.append(pair)
            #print(pairs)
    return pairs


def calc_diff(file1, file2, corr_cols):
    """
    Calculates delta Admixture between the correlating columns.

    :param infile[0]: pandas.DataFrame from Autosomes file
    :param infile[1]: pandas.DataFrame from X chromosomes file
    :param infile[2]: List of pairs representing correlated columns
    :rtype: pandas.DataFrame
    """
    try:
        d =[]
        df = file1
        for i in range(len(corr_cols)):
            col1 = corr_cols[i][0] #column from first file
            col2 = corr_cols[i][1] #column from 2nd file
            c = "diff_of_"+ str(col1) + "_and_" + str(col2) #naming new columns
            df[str(c)] = (file1[col1].astype('float64')-file2[col2].astype('float64'))#/(file1[col1].astype('float64')+file2[col2].astype('float64')) #calculating diff between the two correlating col
            del df[col1]
        #print(df)
        return df
    except Exception as e:
        return "An error has occured at read_file: " + str(e)