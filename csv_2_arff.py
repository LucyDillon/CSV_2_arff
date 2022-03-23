import pandas as pd
import argparse 

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run csv to arff tool parameters')
    parser.add_argument('-csv', action='store', dest='csv', required=True, 
                        help='csv input file')
    parser.add_argument('-option_col', action='store', dest='option_col', required=False, 
                        help='name of option columm, to subset') 
    parser.add_argument('-option_1', action='store', dest='option_1', required=False, 
                        help='subset by specific option name') 
    parser.add_argument('-AB_col', action='store', dest='AB_col', required=False, 
                        help='name of antibiotic columm, to subset') 
    parser.add_argument('-AB_name', action='store', dest='AB_name', required=False, 
                        help='subset by specific antibiotic name')                   
    parser.add_argument('-rel', action='store', dest='relation', 
                        help='relation, how attributes are linked', required=True)
    parser.add_argument('-sample', action='store', dest='sample', 
                        help='sample, column title of where samples/repeats are', required=True)
    parser.add_argument('-n_attr_name', action='store', dest='num_attr_name', 
                        help='Name of numeric attributes column title', required=True)
    parser.add_argument('-n_attr_value', action='store', dest='num_attr_val', 
                        help='Numeric attributes values column title', required=True)
    parser.add_argument('-c_attr_value', action='store', dest='cat_attr_val', 
                        help='Catagorical variable values column values', required=True)
    parser.add_argument('-c_attr_name', action='store', dest='cat_attr_name', 
                        help='Catagorical variable column title', required=True)
    parser.add_argument('-o', action='store', dest='output_file', 
                        help='Name of output file', required=True)

options = parser.parse_args()

# read in data:
data = pd.read_csv(options.csv)

#Subset by specific option (if option selected):
# I used this to subset by specific taxa,this is not needed but may be useful!
try:
    data = data[data[options.option_col] == options.option_name]
except: print('No specific option selected')

    
# reduce dataframe if needed (by selecting only specific columns):
data = data[[options.sample, options.cat_attr_val, options.num_attr_name, options.num_attr_val]]

# reorder data columns, if needed:
data.columns = [options.sample, options.cat_attr_val, options.num_attr_name, options.num_attr_val]

# rename columns:
data.columns = ['samples', 'cat_attr_val', 'num_attr_name', 'num_attr_val']

samples = data.samples.drop_duplicates() # unique list of samples 

num_attr_name = data.num_attr_name.drop_duplicates() # unique list of num attr names

Reduced_data = data.drop(columns=['cat_attr_val'])

Array_df = Reduced_data[["num_attr_name", "samples", "num_attr_val"]]
Array_df = Array_df.drop_duplicates()

Array_of_data= Array_df.pivot_table(index = 'samples',
                                    columns = 'num_attr_name',
                                    values = 'num_attr_val',
                                    fill_value=0)

# Get matching phenotype for the different genome ids:
cata_attr_val = data.drop(columns=['num_attr_name', 'num_attr_val']) #catagorical variable 
cata_attr_val = cata_attr_val.drop_duplicates()
cata_attr_val = cata_attr_val.set_index('samples')

# Add matching catagorical attribiute to main table:
Array_of_data['cat_attr_val'] = cata_attr_val

#Sort the unique list of numeric attributes:
num_attr_name = num_attr_name.sort_values(ascending=True) #unique numeric attribute names

# Make an array of data (in this case gene hits) from the df above:
array_data = Array_of_data.to_string(index=False, header=False)
array_data_sep = array_data.replace(' ', ',')
array_data_sep = array_data_sep.replace(',,,', ',')
array_data_sep = array_data_sep.replace(',,', ',')

# Make an output file:
outfile = options.output_file
att_out = open(outfile, "w")
# Write an attribute list into the first part of the file:
i = options.relation
att_out.write('@RELATION    ' + i +'\n')
for j in num_attr_name:  
    att_out.write("@ATTRIBUTE " + i + "-" + j + "    REAL\n")
name = options.cat_attr_name
att_out.write('@ATTRIBUTE ' + name + '		{Susceptible, Resistant}\n')
att_out.write('@DATA\n')
# Write the array data to the bottom of the file and close the file:
att_out.write(array_data_sep)
att_out.write('\n')
att_out.close()
