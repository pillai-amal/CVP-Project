import torch
import torch.nn as nn
import torch.optim as optim
from tqdm import tqdm
from unet import UNET
from dataset import CVPDataset
from utils import (
    load_checkpoint,
    save_checkpoint,
    get_loaders,
    check_accuracy,
    save_prediction_as_imgs
)

# Hyperparameters
LEARNING_RATE = 1e-4
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
BATCH_SIZE = 50
NUM_EPOCHS = 2
NUM_WORKERS = 2
IMAGE_HEIGHT = 512
IMAGE_WIDTH = 512
PIN_MEMORY = True
LOAD_MODEL = True
TRAIN_IMG_DIR = "data/train_inputs/"
TRAIN_GT_DIR = "data/train_gts/"
VAL_IMG_DIR = "data/val_inputs/"
VAL_GT_DIR = "data/val_gts/"
MODEL_STATE_DIR = "model_state/"
PRED_IMG_DIR = "saved_images/" 


def train_func(loader, model, optimizer, loss_fn, scaler):
    loop = tqdm(loader)
    # model = model.float()
    for batch_idx, (data, targets) in enumerate(loop):
        data = data.to(device=DEVICE)
        targets - targets.unsqueeze(1).to(device=DEVICE)

        #forward
        with torch.cuda.amp.autocast():
            predictions = model(data.float())
            loss = loss_fn(predictions, targets)

        #backward
        
        optimizer.zero_grad()
        scaler.scale(loss).backward()
        scaler.step(optimizer)
        scaler.update()


        loop.set_postfix(loss=loss.item())


def main():
    model = UNET(in_channels=1, out_channels=1).to(DEVICE)
    loss_fn = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)

    train_loader, val_loader = get_loaders(
        TRAIN_IMG_DIR,
        TRAIN_GT_DIR,
        VAL_IMG_DIR,
        VAL_GT_DIR,
        BATCH_SIZE
    )

    scaler = torch.cuda.amp.GradScaler()
    for epoch in range(NUM_EPOCHS):
        train_func(train_loader, model, optimizer, loss_fn, scaler)

        #save model
        checkpoint = {
            "state_dict": model.state_dict(),
            "optimizer": optimizer.state_dict()
        }
        save_checkpoint(checkpoint, epoch, folder=MODEL_STATE_DIR)

        #check accuracy
        check_accuracy(val_loader, model, device=DEVICE)

        save_prediction_as_imgs(
            val_loader,model,folder=PRED_IMG_DIR,device=DEVICE
        )
if __name__ == "__main__":
    main()


