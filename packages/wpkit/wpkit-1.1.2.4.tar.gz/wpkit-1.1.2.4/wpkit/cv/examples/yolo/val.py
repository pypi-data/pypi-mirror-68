import keras
from keras.models import load_model,Model
import os,shutil,glob,random,cv2
from PIL import Image
from scripts.convert_annotations import load_from_plain_annotation
import numpy as np
from yolo3.yolo import YOLO

class YoloPreditor:
    def __init__(self,model_path=None,classes_path=None,classes=None):
        model_path=model_path or ''
        self.model=YOLO(model_path=model_path,classes_path=classes_path)
    def predict(self,img):
        objects=self.model.detect_image(img,with_prob_and_class=True)
        return objects
class YoloValDataLoader:
    def __init__(self,annot_path):
        self.annot_path=annot_path
        self.annots=load_from_plain_annotation(annot_path)
        self.current_index=0
        self.length=len(self.annots)
    def get_pair(self):
        index=self.current_index
        annot=self.annots[index]
        path=annot['path']
        objects=annot['objects']
        # img=cv2.imread(path)
        img=Image.open(path)
        self.current_index+=1
        return img,objects
class Evaluator:
    def __init__(self,classes_path=None,num_classes=20):
        classes=open(classes_path,'r').read().strip().split('\n')
        self.classes=classes
        self.num_classes=len(classes)
        self.totals=[0]*self.num_classes
        self.corrects=[0]*self.num_classes
    def eval(self,preds,labels):
        preds=self.count_plain_objects(preds)
        labels=self.count_dict_objects(labels)
        for i in range(len(labels)):
            if labels[i] or preds[i]:
                self.totals[i]+=1
                if labels[i] and preds[i]:
                    self.corrects[i]+=1
    def summary(self):
        accs=self.accuracies()
        for i in range(len(accs)):
            print('***%s: %s'%(self.classes[i],accs[i]))

    def accuracies(self):
        accs=[None]*self.num_classes
        for i in range(len(self.totals)):
            if self.totals[i]:
                accs[i]=self.corrects[i]/self.totals[i]
        return accs
    def count_dict_objects(self,objects):
        counter = [0] * self.num_classes
        for obj in objects:
            counter[obj['class']]+=1
        return counter
    def count_plain_objects(self,objects):
        counter=[0]*self.num_classes
        for box,prob,cls in objects:
            counter[cls]+=1
        return counter




def val(val_dir=None,val_annots_path=None,classes_path=None,model_path=None):
    if not val_annots_path:
        val_annots_path=os.path.basename(val_dir)+'/val_annotations.txt'
    data_loader=YoloValDataLoader(annot_path=val_annots_path)
    P=YoloPreditor(model_path=model_path,classes_path=classes_path)
    eveluator=Evaluator(classes_path=classes_path)
    for i in range(data_loader.length):
        img,objects=data_loader.get_pair()
        pred_objs=P.predict(img)
        print(pred_objs)
        eveluator.eval(pred_objs,objects)
    eveluator.summary()


if __name__ == '__main__':
    val(
        model_path='logs/000/trained_weights_final.h5',
        classes_path='/home/ars/disk/chaoyuan/dataset/detect_datasets/classes.txt',
        val_annots_path='/home/ars/disk/chaoyuan/dataset/detect_datasets/通用检测/val_annotations.txt'
    )