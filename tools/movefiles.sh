#!/bin/bash

# Source and destination directories
source_dir="/path/to/source_folder"

destination_dir_objects="/path/to/destination_folder"
destination_dir_cloths="/path/to/destination_folder"

if [ ! -d "$source_dir" ]; then
    echo "Source directory does not exist!"
    exit 1
fi

if [ ! -d "$destination_dir_objects" ]; then
    mkdir -p "$destination_dir"
fi

if [ ! -d "$destination_dir_cloths" ]; then
    mkdir -p "$destination_dir"
fi

mv "$source_dir"/*_original.obj "$destination_dir"/
mv "$source_dir"/*_cloth.obj "$destination_dir"/

echo "Files moved successfully!"

