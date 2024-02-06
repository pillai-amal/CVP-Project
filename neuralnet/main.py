import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from model import UNetPixelwiseRegression
from dataset import CustomDataset
from train import train_model

if __name__ == "__main__":
    
    data_folder = "./input"

    batch_size = 20
    patch_size = 33 #hab ich willkurlich jeden Bilden 33x33 Segmentiert  

    # Create DataLoader for batching
    dataset = CustomDataset(data_folder)
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

    # Instantiate the U-Net model
    num_epochs = 5
    criterion = nn.MSELoss()
    model = UNetPixelwiseRegression()
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    train_model(model, dataloader, criterion, optimizer, num_epochs)
    torch.save(model.state_dict(), 'trained_model.pth')

    