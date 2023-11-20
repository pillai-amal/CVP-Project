#!pip install objaverse --upgrade --quiet

import objaverse.xl as oxl
import multiprocessing
import pandas as pd
import requests
import re 


download_directory = "/content/obj"
annotations_df = oxl.get_annotations(download_dir=download_directory)
dataset_df = annotations_df[annotations_df['fileType'] == 'obj'].sample(n=2, random_state=42)

oxl.download_objects(dataset_df, download_directory, multiprocessing.cpu_count())

def download_files(url):
  match = re.search(r'[^/]*$', url)
#this will download the files in the ~ or in case of colab /content/
  destination = match.group(0)
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