import keras
import numpy as np
from keras.models import Model,load_model
from keras.preprocessing import image
from keras import backend as K
import os,cv2,glob

default_weights_path=os.path.dirname(__file__)+'/'+'weights/model.h5'

class Predictor:
    def __init__(self,weights_path=None,classes=None,classes_path=None):
        weights_path=weights_path or default_weights_path
        model = load_model(weights_path)
        self.model=model
        self.tar_imsize = (224, 224)
        if classes_path:
            assert os.path.exists(classes_path)
            classes=open(classes_path,"r",encoding="utf-8").read().strip().split()
        self.classes=classes or ['有效','无效']
    def predict_from_file(self,f):
        im = cv2.imread(f)
        return self.predict(im)
    def predict(self,im):
        if not isinstance(im,np.ndarray):
            im=self.cvimg(im)
        im=self.preprocess(im)
        y=self.model.predict(im)[0]
        return self.decode_y(y)
    def decode_y(self,y):
        k=np.argmax(y)
        return self.classes[k]
    def preprocess(self,im):
        im = cv2.resize(im, self.tar_imsize)
        im = np.array(im).astype(np.float)
        return np.array([im])
    def load_img(self,f):
        im = cv2.imread(f)
        im = cv2.resize(im, self.tar_imsize)
        im = np.array(im).astype(np.float)
        return np.array([im])

    def cvimg(self,x):
        from PIL import Image
        im = x
        x = np.array(x).astype(np.float)
        if isinstance(im, Image.Image) and len(x.shape) == 3: x = x[:, :, ::-1]
        return x
    def print_modeL_structure(self):
        model=self.model
        for i, layer in enumerate(model.layers):
            print(i, layer.name)
def demo_dir(dir='data/imgs/0',sort=False):
    P = Predictor()
    fs=glob.glob(dir+'/*.jpg')
    if sort:
        fs.sort(key=lambda x:int(os.path.basename(x).rstrip('.jpg')))
    for i,f in enumerate(fs):
        y=P.predict_from_file(f)
        print(i,f,y)
def demo():
    P = Predictor()
    # f='data/imgs/0/0.jpg'
    f = 'data/imgs/1/0.jpg'
    y = P.predict_from_file(f)
    print(y)
if __name__ == '__main__':
    demo()