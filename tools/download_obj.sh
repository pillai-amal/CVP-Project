#!/bin/bash

# Check if CSV file is provided as an argument
if [ -z "$1" ]; then
  echo "Usage: $0 <csv_file>"
  exit 1
fi

# Check if wget is installed
if ! command -v wget &> /dev/null; then
  echo "Error: wget is not installed. Please install wget and try again."
  exit 1
fi

# Read CSV file line by line, removing carriage return characters
while IFS= read -r object_link; do
  # Skip the header row (if present)
  if [ "$object_link" != "ObjectLink" ]; then
    # Remove carriage return characters from the object link
    object_link=$(echo "$object_link" | tr -d '\r')
    
    # Download the object using wget
    wget "$object_link"
  fi
done < "$1"

echo "Download completed."
