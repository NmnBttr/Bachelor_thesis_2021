#meanQ A_B_AC autosomes 3. Spalte Khoisan (max werte haben Taa_North,Taa_West und Ju_hoan_North)
#meanQ X_B x chromosomes 2. Spalte Khoisan (max werte haben Taa_North,Taa_West und Ju_hoan_North)

import sys
import pandas as pd
from pylab import *
from scipy.stats import sem
import matplotlib.pyplot as plt
import seaborn as sns

def create_av_Khoisan_table(a_df,x_df,mtDNA_Y_df):
    #print(mtDNA_Y_df)
    Khoisan_df = a_df.merge(x_df,how="inner",on="Population")
    #Khoisan_df =m_df.merge(mtDNA_Y_df,how="inner",on="Population") #m_df[m_df.Population.isin(Khoisan_pops)]
    print(Khoisan_df)
    res = pd.DataFrame()
    mean_A_Khoisan = []
    mean_X_Khoisan = []
    SE_A_Khoisan = [] 
    SE_X_Khoisan = []
    N_col = []
    res["Population"]=Khoisan_df["Population"].unique()
    for c, pop in enumerate(Khoisan_df["Population"].unique()):
        df = Khoisan_df.loc[Khoisan_df['Population']== pop]
        N_col.append(len(df))
        mean_A_Khoisan.append(round(mean(df["A_Khoisan"]),3))
        SE_A_Khoisan.append(round(sem(df["A_Khoisan"]),3))
        mean_X_Khoisan.append(round(mean(df["X_Khoisan"]),3))
        SE_X_Khoisan.append(round(sem(df["X_Khoisan"]),3))
    res["Aut_X_(n)"] = N_col
    res["mean_A_Khoisan"] = mean_A_Khoisan
    res["SE_A_Khoisan"] = SE_A_Khoisan # The standard error of the mean is a way to measure how spread out values are in a dataset.
    res["mean_X_Khoisan"] = mean_X_Khoisan
    res["SE_X_Khoisan"] = SE_X_Khoisan
    res = res.merge(mtDNA_Y_df,how="inner",on="Population")
    return res

def khoisan_plot(df):
    #print(df)
    temp_df = df.reindex(columns=['Population',"mean_A_Khoisan", "mean_X_Khoisan", "freq_L0d_L0k","freq_A2_A3b1_B2b"])
    temp_df = pd.melt(temp_df, id_vars="Population", var_name="markers", value_name="vals")

    temp_df["y_axis"]=pd.DataFrame(np.zeros(temp_df.shape[0])) # dummy column for plotting
    
    custom = [Line2D([], [], marker='o', color='green', linestyle='None'),
          Line2D([], [], marker='x', color='orange', linestyle='None'),
          Line2D([], [], marker='s', color='red', linestyle='None'),
          Line2D([], [], marker='+', color='blue', linestyle='None')]

    fig, axs = plt.subplots(len(temp_df['Population'].unique()), 1, sharex=True, sharey=True, figsize=(20,20)) # set format of subplot grid, share all axes
    fig.subplots_adjust(hspace=0.3, wspace=0.1)
    africa_pop = ["Khomani","Taa_West","Taa_North","Taa_East","Xuun","Ju_hoan_North","Hoan","Ju_hoan_South","Gui","Gana","Nama","Naro","Ani_Buga","Shua","Tshwa","Haiom","Xo","Damara","Mbukushu","Herero","Kgalagadi","Tswana","Himba"]
    for k,pop in enumerate(africa_pop): #(temp_df['Population'].unique()):
        sns.set(style="darkgrid")
        sns.set_context("paper", font_scale=1.5) 
        sns.scatterplot(ax=axs[k],data=temp_df.loc[temp_df['Population']== pop],palette=["green","orange","red","blue"],x="vals",y="y_axis",style="markers",hue="markers",legend=False,s=200,alpha=0.7).set(ylim=(-0.01,0.01),xlim=(0,1),ylabel=None,xlabel=None,yticks=[],xticks=np.arange(0,1.05,0.05))
    
    fig.legend(handles=custom, ## setting legend for all plots
            labels=["Autosome", "X chr", "mtDNA","Y chr"],
            loc="center right",   # Position of legend
            borderaxespad=0.5,    # Small spacing around legend box
            title="Legend",  # Title for the legend
            fontsize="small")

    fig.text(0.5,0.04,'Khoisan Frequency',ha='center',fontsize='large')
    
    plt.show()
    #plt.savefig("khoisan_av.png")
    return


def main(argv):
    if len(argv)!=5:
        print("Input1: autosomal meanQ (A_B_AC);\nInput2: x chr meanQ (X_B);\nInput3: fam_file;\nInput4: mtDNA and Y chr freq file;")
        return
    else:
        # open input files 
        with open(argv[3]) as f:
            fam_df = pd.read_csv(f, sep='\t',usecols=[9],names=["Population"],header=None) # read only population name
        with open(argv[1]) as meanQ_A_file:
            a_df = pd.read_csv(meanQ_A_file, sep='  ',usecols=[2],names=["A_Khoisan"],header=None, dtype='float',engine='python')
            a_df["Population"] = fam_df["Population"]
        with open(argv[2]) as meanQ_X_file:
            x_df = pd.read_csv(meanQ_X_file, sep='  ',usecols=[1],names=["X_Khoisan"],header=None, dtype='float',engine='python')
            x_df["Population"] = fam_df["Population"]
        with open(argv[4]) as f:
            mtDNA_Y_df = pd.read_csv(f, sep=',') # read only population name
        res = create_av_Khoisan_table(a_df,x_df,mtDNA_Y_df)

        #khoisan_plot(res)
        #print(res)
        res.to_csv("average_Khoisan_ancestry_in_Aut_and_X_mtDNA_Y.csv",sep='\t',na_rep='NA')
    return
if __name__ == "__main__":  # pragma: nocover
    main(sys.argv)