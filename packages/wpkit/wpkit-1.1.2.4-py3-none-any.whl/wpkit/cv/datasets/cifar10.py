import torch
from torch.utils.data import DataLoader
from torchvision import transforms,datasets


data_dir='/home/ars/disk/datasets/cifar-10-python'

transform = transforms.Compose(
    [transforms.ToTensor(),
     transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])

trainset=datasets.CIFAR10(data_dir,train=True,transform=transform,download=False)
train_loader=DataLoader(trainset,batch_size=8,num_workers=4)

valset=datasets.CIFAR10(data_dir,train=False,transform=transform,download=False)
val_loader=DataLoader(valset,batch_size=8,num_workers=4,shuffle=False)

