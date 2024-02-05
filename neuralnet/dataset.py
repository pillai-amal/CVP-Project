import os
import numpy as np
import torch
from torch.utils.data import Dataset

class CustomDataset(Dataset):
    def __init__(self, data_folder):
        self.data_folder = data_folder
        self.file_list = [f for f in os.listdir(data_folder) if f.endswith('.npy')]

    def __len__(self):
        return len(self.file_list)

    def __getitem__(self, index):
        file_path = os.path.join(self.data_folder, self.file_list[index])
        input_data = torch.from_numpy(np.load(file_path)).float()  # Ensure the input is of type float
        target_data = torch.from_numpy(np.load(file_path.replace("input", "target"))).float()
        return input_data, target_data
