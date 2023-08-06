import os,shutil,glob,random
import torch,torchvision
from torchvision import datasets, models, transforms
from torch import nn
import torch.optim as optim

train_dir='/home/ars/disk/datasets/car_datasets/stanford/classify_dataset/train'
val_dir='/home/ars/disk/datasets/car_datasets/stanford/classify_dataset/val'
save_path='model.pkl'
num_classes=196
batch_size=8
num_epochs=200
input_size=(228,228)
max_bad_epochs=5
use_pretrained=False
def main():
    model, device, train_loader, val_loader, criterion, optimizer=init()
    model=train(model,device,train_loader,val_loader,criterion,optimizer)
    torch.save(model, 'model.pkl')
    pass

def train(model,device,train_loader,val_loader,criterion,optimizer):
    import time,copy
    model.train()
    dataloaders={
        'train':train_loader,'val':val_loader
    }
    since = time.time()

    val_acc_history = []

    best_model_wts = copy.deepcopy(model.state_dict())
    best_acc = 0.0

    no_improvement_epochs = 0
    for epoch in range(num_epochs):
        print('Epoch {}/{}'.format(epoch, num_epochs - 1))
        print('-' * 10)

        # Each epoch has a training and validation phase
        for phase in ['train', 'val']:
            if phase == 'train':
                model.train()  # Set model to training mode
            else:
                model.eval()  # Set model to evaluate mode

            running_loss = 0.0
            running_corrects = 0

            # Iterate over data.
            for inputs, labels in dataloaders[phase]:
                inputs = inputs.to(device)
                labels = labels.to(device)

                # zero the parameter gradients
                optimizer.zero_grad()

                # forward
                # track history if only in train
                with torch.set_grad_enabled(phase == 'train'):
                    outputs = model(inputs)
                    loss = criterion(outputs, labels)
                    _, preds = torch.max(outputs, 1)
                    # backward + optimize only if in training phase
                    if phase == 'train':
                        loss.backward()
                        optimizer.step()
                # statistics
                running_loss += loss.item() * inputs.size(0)
                running_corrects += torch.sum(preds == labels.data)

            epoch_loss = running_loss / len(dataloaders[phase].dataset)
            epoch_acc = running_corrects.double() / len(dataloaders[phase].dataset)

            print('{} Loss: {:.4f} Acc: {:.4f}'.format(phase, epoch_loss, epoch_acc))

            # deep copy the model
            if phase == 'val':
                if epoch_acc > best_acc:
                    no_improvement_epochs = 0
                    best_acc = epoch_acc
                    best_model_wts = copy.deepcopy(model.state_dict())
                else:
                    no_improvement_epochs += 1
                    if no_improvement_epochs >= max_bad_epochs:
                        import logging
                        logging.info('Stop improving for %s epochs...' % (no_improvement_epochs))
                        break

            if phase == 'val':
                val_acc_history.append(epoch_acc)

    time_elapsed = time.time() - since
    print('Training complete in {:.0f}m {:.0f}s'.format(time_elapsed // 60, time_elapsed % 60))
    print('Best val Acc: {:4f}'.format(best_acc))

    model.load_state_dict(best_model_wts)
    return model, val_acc_history


def init():
    model=models.resnet152(pretrained=use_pretrained)
    num_ftrs = model.fc.in_features
    model.fc = nn.Linear(num_ftrs, num_classes)
    device=torch.device('cuda:0' if torch.cuda.is_available() else'cpu')
    model.to(device)
    data_transforms=get_transform()
    train_transform=data_transforms['train']
    val_transform=data_transforms['val']
    train_dataset=datasets.ImageFolder(root=train_dir,transform=train_transform)
    val_dataset=datasets.ImageFolder(root=val_dir,transform=val_transform)
    train_loader=torch.utils.data.DataLoader(train_dataset, batch_size=batch_size, shuffle=True, num_workers=4)
    val_loader=torch.utils.data.DataLoader(val_dataset, batch_size=batch_size, shuffle=True, num_workers=4)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.SGD(model.parameters(), lr=0.001, momentum=0.9)
    # optimizer = optim.Adam(model.parameters(),lr=0.001)
    return model,device,train_loader,val_loader,criterion,optimizer

def get_transform():
    data_transforms = {
        'train': transforms.Compose([
            transforms.RandomResizedCrop(input_size),
            transforms.RandomHorizontalFlip(),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ]),
        'val': transforms.Compose([
            transforms.Resize(input_size),
            transforms.CenterCrop(input_size),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ]),
    }
    return data_transforms


if __name__ == '__main__':
    main()