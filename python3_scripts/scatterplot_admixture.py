import sys
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pylab import *
from seaborn.relational import scatterplot 
import calculating_differences

def ceildiv(a, b):
    return -(-a // b)

def scatter_plot(df, name,hsize):
    total = len(df["Population"].unique())
    rows = int(floor(sqrt(total)))
    columns = int(ceildiv(total,rows))
    x= np.arange(0,1.5,0.5) # for x & y ticks
    fig, axs = plt.subplots(rows, columns, sharex=True, sharey=True)#,figsize=(0.1,0.1)) # set format of subplot grid, share all axes
    fig.subplots_adjust(hspace=hsize, wspace=0.1) #hspace=0.7 for all pop & 0.35 for african pop
    
    for k,pop in enumerate(df['Population'].unique()):
        pop_data = df.loc[df['Population']== pop]
        sns.set(style="whitegrid")
        sns.set_context("paper", font_scale=0.5) 
        axs[k//columns,k%columns].set(adjustable='box', aspect='equal')
        axs[k//columns,k%columns].plot([0,1],[0,1],ls="-",c='black',alpha=0.7,linewidth=0.8)
        axs[k//columns,k%columns].fill_between((0,1),(0,1),alpha=0.7,color='lightskyblue',linewidth=0.0) # unten rechts
        axs[k//columns,k%columns].fill_between((0,1),(0,1),np.max((0,1)),alpha=0.7,color='lightpink',linewidth=0.0) # oben links 
        
        sns.scatterplot(ax=axs[k//columns,k%columns],data=pop_data,x="Autosome_0",y="Xchr_0",palette="bright",s=2.5,alpha=0.7).set(title=pop,xticks=x,yticks=x,xlabel=None,ylabel=None)
        sns.scatterplot(ax=axs[k//columns,k%columns],data=pop_data,x="Autosome_1",y="Xchr_1",palette="bright",s=2.5,alpha=0.7).set(xlabel=None,ylabel=None)
        sns.scatterplot(ax=axs[k//columns,k%columns],data=pop_data,x="Autosome_2",y="Xchr_2",palette="bright",s=2.5,alpha=0.7).set(xlabel=None,ylabel=None)
        #sns.scatterplot(ax=axs[k//columns,k%columns],data=pop_data,x="Autosome_3",y="Xchr_3",palette="bright",s=2.5,alpha=0.7).set(xlabel=None,ylabel=None)
        axs[k//columns,k%columns].tick_params(axis='both', labelsize=5) #which='major', 

    fig.text(0.5,0.04,'Autosomes',ha='center',fontsize='xx-large')
    fig.text(0.04,0.5,'X chromosome',va='center',rotation='vertical',fontsize='xx-large')
  
    #plt.show()  
    plt.savefig('scatterplot_admixture_'+name, dpi=1200)
    return

def prep_df(a_df,x_df,corr_cols,fam_df):
    for i in range(len(corr_cols)):
        col1 = corr_cols[i][0] #column from first file
        col2 = corr_cols[i][1] #column from 2nd file

        fam_df["Autosome_"+str(i)] = a_df[col1]
        fam_df["Xchr_"+str(i)] = x_df[col2]

    #africa_pop = ['Ani_Buga','Bantu_NE','Bantu_SW','Damara','Gana','Gui','Haiom','Herero','Himba','Hoan','Ju_hoan_North','Ju_hoan_South','Kgalagadi','Khomani','Mbukushu','Nama','Naro','Shua','Taa_East','Taa_North','Taa_West','Tshwa','Tswana','Xo','Xuun']
    #african_df = fam_df[fam_df.Population.isin(africa_pop)]
    print(fam_df)
    return fam_df #, african_df


def main(argv):
    if len(argv)!=4:
        print("Input1: autosomal meanQ; Input2: X chr meanQ; Input3: fam_file")
        return
    else:
        # open input files 
        with open(argv[3]) as f:
            fam_df = pd.read_csv(f, sep=',',usecols=[0,6,9],names=["ID","Continent","Population"],header=None) # read only population name
        with open(argv[1]) as meanQ_A_file:
            a_df = pd.read_csv(meanQ_A_file, sep=' ',header=None, dtype='float',engine='python')
        with open(argv[2]) as meanQ_X_file:
            x_df = pd.read_csv(meanQ_X_file, sep=' ',header=None, dtype='float',engine='python')
        
        # get correlating columns from autosome and x chr files
        corr_colm = calculating_differences.get_corr_col(a_df,x_df) 
        # print(corr_colm)
        # round autosome and x chr df's for plotting
        for column in a_df:
            a_df[column] = a_df[column].round(decimals=2)
        for column in x_df:
            x_df[column] = x_df[column].round(decimals=2)
        
        # prepare files for plotting
        df = prep_df(a_df,x_df,corr_colm,fam_df)
        #print(df[1])
        scatter_plot(df,"ALL_POP",0.7)
        #scatter_plot(df[1],"African_POP",0.35)


if __name__ == "__main__":  # pragma: nocover
    main(sys.argv)