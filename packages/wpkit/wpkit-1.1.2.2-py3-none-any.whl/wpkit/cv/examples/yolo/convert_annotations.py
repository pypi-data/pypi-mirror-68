
import os,shutil,glob,random,cv2,json
from PIL import Image
from wpkit.utils import json_load,json_dump,copy_files_to,remake

'''
plain: path l,t,r,b,cls l,t,r,b,cls ....
'''

def load_from_plain_line(line=''):
    parts=line.split()
    path=parts[0]
    objs=parts[1:]
    dic={}
    dic['path']=path
    objects=[]
    for obj in objs:
        box=obj.split(',')
        box=[int(x) for x in box]
        obj={'class':box[-1],'bbox':box[:-1]}
        objects.append(obj)
    dic['objects']=objects
    return dic
def load_from_plain_annotation(path):
    with open(path,'r') as f:
        lines=f.read().strip().split('\n')
    lines=[load_from_plain_line(line) for line in lines]
    return lines
def dump_to_plain_line(annot):
    path=annot['path']
    objs=annot['objects']
    objects=[]
    for obj in objs:
        obj=[*obj['bbox'],obj['class']]
        obj=[str(x) for x in obj]
        obj=','.join(obj)
        objects.append(obj)
    objects=[path,*objects]
    line=' '.join(objects)
    return line
def dump_to_plain_annotation(annots,path):
    annots=[dump_to_plain_line(annot) for annot in annots]
    annots='\n'.join(annots)
    with open(path,'w') as f:
        f.write(annots)

def convert_from_plain_to_jsonannot(path,path2):
    dic=load_from_plain_annotation(path)
    dump_to_plain_annotation(dic,path2)
def convert_from_jsonanoot_to_plain(path,path2):
    dic=json_load(path)
    dump_to_plain_annotation(dic,path2)


def alter_annots_base(annots,dst):
    for annot in annots:
        annot['path']=dst+'/'+os.path.basename(annot['path'])
    return annots

def make_yolo_datasets_from_plain_annots(annot_path,out_dir=None,train_dir=None,val_dir=None,train_annots_path=None,val_annots_path=None,val_split=0.1,val_num=None):
    '''

    '''
    if not train_dir:
        train_dir=out_dir+'/train'
    if not val_dir:
        val_dir=out_dir+'/val'
    if not train_annots_path:
        train_annots_path=out_dir+'/train_annotations.txt'
    if not val_annots_path:
        val_annots_path=out_dir+'/val_annotations.txt'

    remake(train_dir)
    remake(val_dir)

    annots=load_from_plain_annotation(annot_path)
    print(annots)
    num=len(annots)
    if not val_num:
        val_num=int(num*val_split)
    random.shuffle(annots)
    train_annots=annots[:-val_num]
    val_annots=annots[-val_num:]
    train_imgs=[annot['path'] for annot in train_annots]
    val_imgs=[annot['path'] for annot in val_annots]
    copy_files_to(train_imgs,train_dir)
    copy_files_to(val_imgs,val_dir)
    train_annots=alter_annots_base(train_annots,train_dir)
    val_annots=alter_annots_base(val_annots,val_dir)
    dump_to_plain_annotation(train_annots,train_annots_path)
    dump_to_plain_annotation(val_annots,val_annots_path)
    print('finished.')


if __name__ == '__main__':
    make_yolo_datasets_from_plain_annots(
        annot_path='/home/ars/disk/chaoyuan/dataset/more_datasets/通用检测v2/annotations.txt',
        out_dir='/home/ars/disk/chaoyuan/dataset/detect_datasets/通用检测'
    )