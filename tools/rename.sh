#!/bin/bash

directory_path="/path/to/your/directory"

if [ ! -d "$directory_path" ]; then
    echo "Directory not found."
    exit 1
fi

# Change to the directory
cd "$directory_path" || exit

# Get the list of files in the directory
file_list=(*)

# Get the number of files
num_files=${#file_list[@]}

# Rename files
for ((i=0; i<num_files; i++)); do
    original_name="${file_list[$i]}"
    new_name="$i"
    
    # Rename the file
    mv "$original_name" "$new_name"
    
    echo "Renamed: $original_name -> $new_name"
done

echo "Files have been renamed in ascending order from 0 to $((num_files-1))."

