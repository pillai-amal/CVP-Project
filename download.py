import objaverse
import objaverse.xl as oxl
import os
import multiprocessing
import pandas as pd
import requests
import re 

# print(os.getcwd())
def download_files(url, dest_dir):
  match = re.search(r'[^/]*$', url)
  destination = os.path.join(dest_dir+match.group(0))
  try:
    response = requests.get(url)
    if response.status_code == 200:
        with open(destination, 'wb') as file:
            file.write(response.content)
        print(f"File downloaded successfully as {destination}")
    else:
        print("Failed to download the file")
  except:
    print("Invalid URL")
    pass
if __name__ == "__main__":
    download_directory = "raw/"
    obj_dir = "obj/"
    if not os.path.exists(download_directory):
        # Create the directory if it doesn't exist
        os.makedirs(download_directory)
        print(f"Directory '{download_directory}' created successfully.")
    else:
        print(f"Directory '{download_directory}' already exists.")

    if not os.path.exists(obj_dir):
        # Create the directory if it doesn't exist
        os.makedirs(obj_dir)
        print(f"Directory '{obj_dir}' created successfully.")
    else:
        print(f"Directory '{obj_dir}' already exists.")

    ## Actual download
    annotations_df = oxl.get_annotations(download_dir=download_directory)
    dataset_df = annotations_df[annotations_df['fileType'] == 'obj'].sample(n=100, random_state=42)
    oxl.download_objects(dataset_df, download_directory, multiprocessing.cpu_count())
    dataset_df['fileIdentifier'].apply(lambda x: download_files(x,obj_dir))