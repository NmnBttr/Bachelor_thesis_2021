import calculating_differences
import argparse
import sys
import os.path

def is_valid_file(parser, arg): # check if input files are valid
    if not os.path.exists(arg):
        parser.error("The file %s does not exist!" % arg)
    else:
        return

parser = argparse.ArgumentParser(
      prog='Calculating differences from two fastSTRUCTURE output meanQ-files.',
      formatter_class=argparse.RawDescriptionHelpFormatter,
      epilog='''\
         Give always path to input file 1 (Autosomes) first and then input file 2 (Xchr)!
         ''')

parser.add_argument("--input","-i", required=True,
                    help="insert path to meanQ files", metavar="FILE", nargs=2,
                    type=lambda x: is_valid_file(parser, x))
parser.add_argument("--output","-o", required=True,
                    help="name output delta admixture calculated file.csv", metavar="FILENAME", nargs=1,
                    )
def main(argv):
    try:
        if len(sys.argv) == 6:
            print('hier drinne')
            filename1 = argv[2]
            filename2 = argv[3]
            outputfile = argv[5]
            file1 = calculating_differences.read_file(filename1)
            file2 = calculating_differences.read_file(filename2)
            corr_columns = calculating_differences.get_corr_col(file1,file2)
            #print(corr_columns)
            df_diff = calculating_differences.calc_diff(file1, file2, corr_columns)
            #df_diff.to_csv(outputfile,index=False,sep='\t')
            print(outputfile + " is now created.")
        else:
            print("An error has occured: Number of given argument is insufficient")
            parser.print_help()
    except Exception as e:  # pragma: nocover
        return "An error has occured: " + str(e)
    return 

if __name__ == "__main__":  # pragma: nocover
    main(sys.argv)