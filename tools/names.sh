#!/bin/bash

# Set the output Python file name
output_file="file_list.py"

# Get the list of all files in the current directory
files=$(ls *)

# Write the Python list to the output file
echo "file_list = [" > "$output_file"
for file in $files
do
    echo "    '$file'," >> "$output_file"
done
echo "]" >> "$output_file"

echo "File list saved to $output_file"

