import os
import torch
from torch.utils.data import Dataset
from PIL import Image
import numpy as np

class CustomDataset(Dataset):
    def __init__(self, data_folder):
        self.data_folder = data_folder
        self.file_list = [f for f in sorted(os.listdir(data_folder)) if f.endswith('.png')]

    def __len__(self):
        return len(self.file_list)

    def __getitem__(self, index):
        file_path = os.path.join(self.data_folder, self.file_list[index])
        
        # Load PNG image using PIL (Pillow)
        input_image = Image.open(file_path).convert('L')  # 'L' mode for grayscale
        
        # Convert PIL image to a PyTorch tensor
        input_data = torch.from_numpy(np.array(input_image)).unsqueeze(0).float()  # Add channel dimension

        # Assuming the target file has the same name with 'target' instead of 'input'
        target_path = os.path.join(self.data_folder, self.file_list[index].replace("input", "target"))
        target_image = Image.open(target_path).convert('L')  # 'L' mode for grayscale
        target_data = torch.from_numpy(np.array(target_image)).unsqueeze(0).float()  # Add channel dimension
        return input_data, target_data
