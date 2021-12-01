# Bachelor thesis 
## *"Inferring sex-biased process in population histories using comparisons between autosomal and X chromosomes"* 
This repository contains all my bash commands and python3 scripts to create the results of this thesis.

## Getting Started

These instructions will get you a copy of the project and how to get to run the scripts on your local machine for testing purposes. 

### Prerequisites and Installing

Please clone the repository Bachelor_thesis_2021 on git and navigate to the directory:

```
$ git clone https://github.com/NmnBttr/Bachelor_thesis_2021.git
$ cd Bachelor_thesis_2021
```

For running the python scripts Python >= 3.6.0 is required and follow the terminal instructions. For example use pipenv for installing the required packages:

```
$ pipenv --python python3
```

### Recreating the results

**Steps:**
1. Data Pre-processing and Filtering

> /bash_scripts/data_filtering.sh

2. Splitting the dataset

> /bash_scripts/data_splitting.sh

3. Running fastSTURTURE using Snakemake + get empty K's + get optimal K

> /bash_scripts/run_fastSTRUCTURE_get_emptyK_chooseK.sh

4. PONG plot for fastSTRUCTURE output

> /bash_scripts/pong_plotting.sh

5. Finding the optimal match between autosomes and X chromosome runs.

```$ python3 match_aut_with_x.py```

6. Calculating difference of the admixture estimation for matching autosomes and X chromosome runs.

```$ python3 calc_diff_client.py```

7. Plotting scatter plot for visualising Step 6.

```$ python3 scatterplot_admixture.py```

8. Calculate average difference per pop separately for BD, FD and MD difference files from Step 6.

```$ python3 calc_av_per_pop.py```

9. Bar plot fo comparing sex-bias estimates across datasets BD, FD and MD. Use output files from Step 8.

```$ python3 comparing_B_F_M_barplot.py```

10. Comparing sex-bias estimates across different markers (creating table + plot)

```$ python3 average_Khoisan.py```

## Author

**Namuun Battur** (email: *namuub98@zedat.fu-berlin.de*)

Supervisor of this project: **Dr. Vladimir Bajić**

## Acknowledgments
I am thankful for the inspiration and continuous help from my supervisor Dr. Bajić.
