import torch
from torch.utils.data import dataloader
from torchvision import models,datasets,transforms
from PIL import Image
import os,shutil,glob,random
def val(data_dir,model_path):
    # load model
    # load data
    # predict
    # count
    model=torch.load(model_path)
    device=torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    model.to(device)
    model.eval()
    val_transform=transforms.Compose([
            transforms.Resize(224),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])
    val_dataset=datasets.ImageFolder(data_dir,transform=val_transform)
    val_loader=dataloader.DataLoader(val_dataset,batch_size=1)
