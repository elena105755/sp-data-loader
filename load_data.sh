#!/bin/bash

# Get the path to the directory containing the CSV files
data_dir="data"

# Iterate over all CSV files in the directory
for file in ./"$data_dir"/*.csv
do
  # Run the load_data.py script for each file
  python3 load_data.py "$file"
done
