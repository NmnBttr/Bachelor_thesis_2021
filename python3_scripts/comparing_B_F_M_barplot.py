import sys
import pandas as pd
import matplotlib.pyplot as plt 
from pylab import *
import seaborn as sns
from matplotlib.patches import Patch # used for custom legends

### this script is for plotting grouped bar plot for comparing average difference between 
### Both, FemalesOnly and MalesOnly files 

def ceildiv(a, b):
    return -(-a // b)

def get_col_corr(av_diff1,av_diff2,av_diff3):
    ### get correlation of F and M columns with the B file columns ### 
    av_df1 = av_diff1.drop(columns=['Population'])
    av_df2 = av_diff2.drop(columns=['Population'])
    av_df3 = av_diff3.drop(columns=['Population'])

    res1=[]
    col_names1 = []
    res2=[]
    col_names2 = []

    for col1 in av_df1.columns:
        for col2 in av_df2.columns:
            res1.append(av_df1[col1].astype('float64').corr(av_df2[col2].astype('float64')))
            col_names1.append(col1)
            col_names1.append(col2)
    print(res1,col_names1)

    for col1 in av_df1.columns:
        for col2 in av_df3.columns:
            res2.append(av_df1[col1].astype('float64').corr(av_df3[col2].astype('float64')))
            col_names2.append(col1)
            col_names2.append(col2)
    print(res2,col_names2)
    return

def main(argv):
    if len(argv)!= 5:
        print("Input1: avergae diff per pop file B;\n Input2: avergae diff per pop file F;\n Input3: average diff per pop file M; \n Input4: outputname for plot name")
        return
    else:
        num_diff1 = pd.DataFrame() ## for saving number of individuals
        num_diff2 = pd.DataFrame()
        num_diff3 = pd.DataFrame() 
        with open(argv[1]) as av_diff_file_B:
            av_diff1 = pd.read_csv(av_diff_file_B, sep=',',header=0)
            num_diff1["N_B"] = av_diff1.iloc[:,1]
            num_diff1['Population'] = av_diff1['Population']
            av_diff1.drop(av_diff1.columns[1],axis=1,inplace=True)
        with open(argv[2]) as av_diff_file_F:
            av_diff2 = pd.read_csv(av_diff_file_F, sep=',',header=0)
            num_diff2["N_F"] = av_diff2.iloc[:,1]
            num_diff2['Population'] = av_diff2['Population']
            av_diff2.drop(av_diff2.columns[1],axis=1,inplace=True)
        with open(argv[3]) as av_diff_file_M:
            av_diff3 = pd.read_csv(av_diff_file_M, sep=',',header=0)
            num_diff3["N_M"] = av_diff3.iloc[:,1]
            num_diff3['Population'] = av_diff3['Population']
            av_diff3.drop(av_diff3.columns[1],axis=1,inplace=True)
    
    # get_col_corr(av_diff1,av_diff2,av_diff3)

    ### column names for F and M are determined manually by getting the maximal correlating column for each B column without duplication while matching
    ### B file columns stays at is and only F and M columns are reordered
    column_names_F = ["Population","F_col_0", "F_col_2", "F_col_1"]
    av_diff2 = av_diff2.reindex(columns=column_names_F)
    column_names_M = ["Population","M_col_1", "M_col_0", "M_col_2"]
    av_diff3 = av_diff3.reindex(columns=column_names_M)

    m_av = av_diff1.merge(av_diff2, how="inner", on="Population")
    merged_av = m_av.merge(av_diff3, how="inner", on="Population") # merged df of all tree average difference files 
    
    pop_num_of_ind  = num_diff1.merge(num_diff2, how="inner", on="Population") # saving number of individuals
    pop_num_of_ind  = pop_num_of_ind.merge(num_diff3, how="inner", on="Population")

    ### Plotting average diff 
    total = merged_av.shape[0]
    rows = int(floor(sqrt(total)))
    columns = int(ceildiv(total,rows))

    ## for custom color and legend
    my_palette = { 
        "AB_AC_XB":"tab:red",
        "AF_AC_XF":"tab:green",
        "AM_AC_XM":"tab:blue",}
    legend_elements = [
        Patch(facecolor='tab:red', edgecolor='black',label='BD'),
        Patch(facecolor='tab:green', edgecolor='black',label='FD'),
        Patch(facecolor='tab:blue', edgecolor='black',label='MD'),]
    fig, axs = plt.subplots(rows, columns, sharex=True, sharey=True, figsize = (7,5))# set format of subplot grid, share all axes
    fig.subplots_adjust(hspace=0.3, wspace=0.1) #
    for k,pop in enumerate(merged_av['Population']): # creating subplots for each population
        sns.set(style="darkgrid")
        sns.set_context("paper", font_scale=1.3) 
        ### Preparing and transforming dataframe for plotting
        df = merged_av.loc[merged_av['Population']== pop]
        temp_df = pd.DataFrame(columns=["col","AB_AC_XB","AF_AC_XF","AM_AC_XM"])
        colA = []
        colB = []
        colC = []
        colD = []
        for i in range(av_diff1.shape[1]-1):
            colA.append("av"+str(i))
            colB.append(df.iloc[0,i+1])
            colC.append(df.iloc[0,i+(av_diff1.shape[1])])
            colD.append(df.iloc[0,df.shape[1]-i-1])
        colD.reverse()
        temp_df["col"]=colA
        temp_df["AB_AC_XB"]=colB
        temp_df["AF_AC_XF"]=colC
        temp_df["AM_AC_XM"]=colD
        t_df = pd.melt(temp_df, id_vars="col", var_name="diff_file", value_name="av_diff") ## this format is needed for plotting grouped bar plots
        
        row_with_N = pop_num_of_ind.iloc[k] ## getting number of individuals
        ax = sns.barplot(ax=axs[k//columns,k%columns],x="col",y="av_diff",hue ="diff_file",data=t_df,palette=my_palette).set(xlabel=None,ylabel=None,title=pop,xticklabels=["A_Pop1","A_Pop2","A_Pop3"],)
        axs[k//columns,k%columns].tick_params(axis='both', labelsize=10)
        axs[k//columns,k%columns].text(0.01, 0.01, "N_F="+ str(row_with_N['N_F'])+"; N_M="+str(row_with_N['N_M']), horizontalalignment='left', verticalalignment='bottom',fontsize="x-small", transform=axs[k//columns,k%columns].transAxes)
        axs[k//columns,k%columns].axhline(0.05, ls='--',c='red')
        axs[k//columns,k%columns].axhline(-0.05, ls='--',c='red')

        for ax in fig.axes: # removing subplot legends and adding line on  x axis
            ax.axhline(0, ls='-')
            Line, Label = ax.get_legend_handles_labels()
            if len(Line) & len(Label) == 0:
                continue
            else:
                ax.legend().remove()
    fig.legend(handles=legend_elements, ## setting legend for all plots
            loc="center right",   # Position of legend
            borderaxespad=0.5,    # Small spacing around legend box
            title="Legend",  # Title for the legend
            )

    fig.text(0.5,0.04,'Ancestry Populations',ha='center',fontsize='xx-large')
    fig.text(0.04,0.5,'Average difference',va='center',rotation='vertical',fontsize='xx-large')
    #plt.show()
    #plt.savefig(argv[4], dpi=1200)
    print(merged_av)
    return

if __name__ == "__main__":  # pragma: nocover
    main(sys.argv)


