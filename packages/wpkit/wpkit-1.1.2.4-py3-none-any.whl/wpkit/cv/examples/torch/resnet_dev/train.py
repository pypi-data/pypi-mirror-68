from torchvision.models.resnet import resnet18,resnet50,resnet34,resnet101,resnet152,resnext101_32x8d,resnext50_32x4d
import torch
from torch import optim,nn
from torch.utils.data import dataloader
from torchvision import transforms,datasets
import os,shutil,glob

def main():
    train(
        data_dir='/home/ars/disk/chaoyuan/dataset/classify_datasets/安全带紧扣',
        model_save_path='model.pkl',
        model_type='resnet50',
        num_epochs=200,
    )

resnet_models=dict(
    resnet18=resnet18,resnet34=resnet34,resnet50=resnet50,
    resnet101=resnet101,resnet152=resnet152,resnext50_32x4d=resnext50_32x4d,resnext101_32x8d=resnext101_32x8d
)
def train(
        data_dir=None,train_dir=None,batch_size=32,num_epochs=50,patience=50,num_classes=None,val_dir=None,model_save_dir=None,model_save_path=None,pretrained_model_path=None,model_type='resnet50',use_default_pretrained_or_download=True
):
    if not train_dir:
        train_dir=data_dir+'/train'
    if not val_dir:
        val_dir=data_dir+'/val'
    if not num_classes:
        num_classes=len(os.listdir(train_dir))
    if not model_save_path:
        model_save_path=model_save_dir+'/model.pkl'
    if pretrained_model_path:
        model=torch.load(pretrained_model_path)
    else:
        model_type=resnet_models[model_type]
        model=model_type(pretrained=use_default_pretrained_or_download)
        in_features=model.fc.in_features
        model.fc=torch.nn.Linear(in_features,num_classes)
    device=torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    model.to(device)
    data_transforms = {
        'train': transforms.Compose([
            transforms.RandomResizedCrop(224),
            transforms.RandomHorizontalFlip(),
            # transforms.ColorJitter(brightness=0.5, contrast=0.5, hue=0.5),
            # transforms.RandomRotation(20),
            transforms.ToTensor(),
            # transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
            transforms.Normalize([0.5, 0.5, 0.5], [0.229, 0.224, 0.225])
        ]),
        'val': transforms.Compose([
            transforms.Resize(224),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ]),
    }
    image_datasets={'train':datasets.ImageFolder(train_dir,transform=data_transforms['train']),
                    'val':datasets.ImageFolder(val_dir,transform=data_transforms['val'])}
    dataloaders={x:dataloader.DataLoader(image_datasets[x],batch_size=batch_size,shuffle=True,num_workers=4) for x in ['train','val']}
    optimizer = optim.SGD(model.parameters(), lr=0.001, momentum=0.9)
    # optimizer=optim.Adam(model.parameters(),lr=0.001)
    # scheduler = optim.lr_scheduler.StepLR(optimizer,  step_size=7, gamma=0.1)
    criterion=nn.CrossEntropyLoss()
    best_acc = 0.0
    bad_epochs=0
    for epoch in range(num_epochs):
        log_info=[]
        for phase in ['train','val']:
            if phase=='train':
                model.train()
            else:
                model.eval()
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
                    _, preds = torch.max(outputs, 1)
                    loss = criterion(outputs, labels)

                    # backward + optimize only if in training phase
                    if phase == 'train':
                        loss.backward()
                        optimizer.step()

                # statistics
                running_loss += loss.item() * inputs.size(0)
                running_corrects += torch.sum(preds == labels.data)
            # if phase == 'train':
            #     scheduler.step()

            epoch_loss = running_loss / len(dataloaders[phase].dataset)
            epoch_acc = running_corrects.double() / len(dataloaders[phase].dataset)

            log_info.append('{} Loss: {:.4f} Acc: {:.4f}'.format(
                phase, epoch_loss, epoch_acc))

            # deep copy the model
            if phase == 'val':
                if epoch_acc > best_acc:
                    bad_epochs=0
                    best_acc = epoch_acc
                    torch.save(model,model_save_path)
                    print('New best model saved to %s'%(model_save_path))
                else:
                    if best_acc>=0.5:
                        bad_epochs+=1
                    if bad_epochs>=patience:
                        print("Val accuracy stopped improving, stop training, best accuracy: %s , model was saved at %s"%(best_acc,model_save_path))
                        return
        print('\t'.join(log_info))



if __name__ == '__main__':
    main()

