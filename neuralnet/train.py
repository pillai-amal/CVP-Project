import torch
from tqdm import tqdm
import torch.nn.functional as F

def train_model(model, dataloader, criterion, optimizer, num_epochs):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)

    for epoch in range(num_epochs):
        model.train()  # Set the model to training mode
        total_loss = 0.0

        with tqdm(total=len(dataloader), desc=f'Epoch {epoch+1}/{num_epochs}', unit='batch') as pbar:
            for inputs, targets in dataloader:
                inputs, targets = inputs.to(device), targets.to(device)
                
                optimizer.zero_grad()
                outputs = model(inputs)
                target_resized = F.interpolate(targets, size=outputs.size()[2:], mode='nearest')

                loss = criterion(outputs, target_resized)
                loss.backward()
                optimizer.step()

                total_loss += loss.item()
                pbar.set_postfix(loss=f'{loss.item():.4f}')
                pbar.update()

        average_loss = total_loss / len(dataloader)
        print(f'Epoch {epoch+1}/{num_epochs}, Average Loss: {average_loss:.4f}')
