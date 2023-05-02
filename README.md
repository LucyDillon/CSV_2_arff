# CSV_2_arff
Convert csv dataframes into .arff file format for use on Weka machine learning. 

General usage:

python csv_2_arff.py -csv input_file.csv -n_attr_name Numeric_attribute_name -n_attr_value Numeric_attribute -c_attr_value Catagorical_attribute_column -c_attr_name Catagorical_attribute -rel How_num_attributes_are_related -sample Sample_column -o my_output_file.arff


Useful notes:
If your column names have spaces between words e.g. "My column" put quotation marks around when writing the code above. 

If there are duplicates of the same sample and numeric/catagorical attributes the tool may produce errors and not run. To avoid this just remove duplicate lines in file.

It you would like to use in a for loop: (using example headings)

``` 
for i in *RGI_specific_genes.csv; do 
	python Universal_csv_2_arff.py -csv $i  -rel Gene -sample genome_id -n_attr_name Gene -n_attr_value GeneHit -c_attr_value add_phenotype -c_attr_name add_phenotype -o $i.arff; 
done 
  
