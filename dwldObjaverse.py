import objaverse
import objaverse.xl as oxl
import multiprocessing
from tqdm import tqdm
import pandas as pd

download_directory = "~/.cvp-dataset"
annotations_df = oxl.get_annotations(download_dir=download_directory)
dataset_df = annotations_df[annotations_df['fileType'] == 'obj'].sample(n=100, random_state=42)

def download_with_progress(obj_info):
    oxl.download_object(obj_info, download_directory)
    pbar.update()

with tqdm(total=len(dataset_df), desc="Downloading Objects", unit="object") as pbar:
    with multiprocessing.Pool() as pool:
        pool.map(download_with_progress, dataset_df.iterrows())
