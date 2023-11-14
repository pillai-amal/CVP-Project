import objaverse
import objaverse.xl as oxl
import multiprocessing
import pandas as pd

download_directory = "~/.cvp-dataset"
annotations_df = oxl.get_annotations(download_dir=download_directory)
dataset_df = annotations_df[annotations_df['fileType'] == 'obj'].sample(n=100, random_state=42)

oxl.download_objects(dataset_df, download_directory)
