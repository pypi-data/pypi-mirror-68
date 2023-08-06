import pickle
from PIL import Image
import os,shutil,glob

def load_list_from_string_v2(text='',template=[list,'\n']):
    '''
    # [list,'\n',[dict,' ',[list,' ',[list,',']]]]
    '''
    if not template:
        return text
    assert isinstance(template, (list, tuple, set))
    length = len(template)
    next_template=None
    cls = template[0]
    if length==1:
        return cls(text)
    else:
        if cls in [list,set,tuple]:
            assert length>=2
            splitchar=template[1]
            if length>=3:
                next_template=template[2]
            items=text.split(splitchar)
            if next_template:
                for i,item in enumerate(items):
                    items[i]=load_list_from_string_v2(item,next_template)
            items=cls(items)
            return items
        elif cls in [dict]:
            assert length >= 3
            item_split=template[1]
            kv_split=template[2]
            if length>=4:
                next_template=template[3]
            dic={}
            items=text.split(item_split)
            for item in items:
                k,v =item.split(kv_split,maxsplit=1)
                if next_template:
                    v = load_list_from_string_v2(v, next_template)
                dic[k]=v
            return dic
class Cifar():
    def __init__(self, batchpath, root="data"):
        self.batchpath = batchpath
        self.root = root
        self.img_label = []

    def make_file_list(self, filename):
        with open(filename, 'a+') as f:
            for (imgname, label) in self.img_label:
                f.writelines("{}\t{}\n".format(imgname, label))

    def data_parse(self):
        with open(self.batchpath, 'rb') as fb:
            cifar_dict = pickle.load(fb, encoding='latin1')
            batch_label, labels, data, filenames = cifar_dict['batch_label'], cifar_dict['labels'], \
                                                   cifar_dict['data'], cifar_dict['filenames']
            for i, (img, label, filename) in enumerate(zip(data, labels, filenames)):
                img = img.reshape(3, 32, 32)
                r = Image.fromarray(img[0]).convert('L')
                g = Image.fromarray(img[1]).convert('L')
                b = Image.fromarray(img[2]).convert('L')
                img = Image.merge('RGB', (r, g, b))

                self._save_img(self.root, img, label, filename)

    def _save_img(self, root, img, label, filename):
        save_path = os.path.join(root, str(label))
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        save_name = os.path.join(save_path, filename)
        save_name = save_name.replace('.png', '.jpg')
        self.img_label.append((save_name, label))

        print(save_name)
        img.save(save_name)
def convert_one(src_path,dst_path,label_path):
    cifar = Cifar(src_path,dst_path)
    cifar.data_parse()
    cifar.make_file_list(label_path)

def convert(src_dir,dst_dir):
    batches=['data_batch_%s'%i for i in range(1,6)]+['test_batch']
    if os.path.exists(dst_dir):
        shutil.rmtree(dst_dir)
        tmp=1+2
    os.makedirs(dst_dir)

    for batch in batches:
        src_bacth_path=src_dir+'/'+batch
        dst_batch_dir=dst_dir+'/'+batch
        dst_label_file=dst_dir+'/'+batch+'.txt'
        os.makedirs(dst_batch_dir)
        convert_one(src_bacth_path,dst_batch_dir,dst_label_file)

def merge(src_dir,dst_dir):
    if os.path.exists(dst_dir):
        shutil.rmtree(dst_dir)
        a=1
    os.makedirs(dst_dir)
    label_files=glob.glob(src_dir+'/*.txt')
    files={}
    for f in label_files:
        dic=load_list_from_string_v2(open(f).read().strip(),template=[dict,'\n','\t'])
        files.update(dic)
    for i,f in enumerate(files.keys()):
        cls=files[f]
        cls_dir=dst_dir+'/'+cls
        if not os.path.exists(cls_dir):
            os.makedirs(cls_dir)
        f2=cls_dir+'/%s.jpg'%i
        shutil.copy(f,f2)
        print(i,f2)




if __name__ == "__main__":
    convert(
        src_dir='/home/ars/disk/datasets/cifar-10-python/cifar-10-batches-py',
        dst_dir='/home/ars/disk/datasets/cifar-10-python/cofar10-reformatted'
    )
    merge(
        src_dir='/home/ars/disk/datasets/cifar-10-python/cofar10-reformatted',
        dst_dir='/home/ars/disk/datasets/cifar-10-python/cofar10-imagenet-format'
    )