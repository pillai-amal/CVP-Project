import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from tqdm import tqdm
from model import UNetPixelwiseRegression
from dataset import CustomDataset

if __name__ == "__main__":
    
    data_folder = "/home/parallels/Documents/CVP/CVP-Project/neuralnet/images/input"

    batch_size = 20
    in_channels = 1
    out_channels = 1
    patch_size = 33 #hab ich willkurlich jeden Bilden 33x33 Segmentiert  

    input_data = torch.randn(batch_size, in_channels, patch_size, patch_size)
    target_data = torch.randn(batch_size, out_channels, patch_size, patch_size)

    # Create DataLoader for batching
    dataset = CustomDataset(data_folder)
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

    # Instantiate the U-Net model
    model = UNetPixelwiseRegression(in_channels, out_channels)

    # Define loss function and optimizer
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)