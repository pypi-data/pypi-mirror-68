from yolo import YOLO, detect_video
from PIL import Image
import os,glob,shutil
import cv2
def demo():
    imgs_dir = '/home/ars/disk/chaoyuan/dataset/detect_datasets/通用检测/val'
    # out_dir = '/home/ars/disk/chaoyuan/dataset/more_datasets/通用检测v2/val_results'
    out_dir=None
    if not out_dir:
        out_dir=imgs_dir+'_results'
    config = dict(
        model_path='logs/000/trained_weights_final.h5',
        classes_path='/home/ars/disk/chaoyuan/dataset/classes.txt'
    )

    # imgs_dir = '/home/ars/disk/chaoyuan/dataset/车辆检测/val'
    # out_dir = '/home/ars/disk/chaoyuan/dataset/车辆检测/val_results'
    # config = dict(
    #     model_path='logs/000/trained_weights_final.h5',
    #     classes_path='/home/ars/disk/chaoyuan/dataset/yolo_labels/classes.txt'
    # )
    #
    # imgs_dir = '/home/ars/disk/chaoyuan/dataset/三角架/val'
    # out_dir = '/home/ars/disk/chaoyuan/dataset/三角架/val_results'
    # config = dict(
    #     model_path='logs/000/trained_weights_final.h5',
    #     # model_path='logs/000/trained_weights_stage_1.h5',
    #     classes_path='/home/ars/disk/chaoyuan/dataset/yolo_labels/classes.txt'
    # )

    # imgs_dir='/home/ars/disk/chaoyuan/文本相关/行驶证'
    # imgs_dir='/home/ars/disk/chaoyuan/文本相关_merge_all'
    # config=dict(
    #     model_path='weights/表头检测/trained_weights_final.h5',
    #     classes_path='/home/ars/work/trainval/行驶证检测/annotations/classes.txt'
        # model_path='weights/行驶证检测/trained_weights_final.h5',
        # model_path='weights/表头检测/trained_weights_final.h5',
        # classes_path='/home/ars/work/trainval/行驶证检测/annotations/classes.txt'
        # classes_path='/home/ars/work/trainval/表头检测/annotations/classes.txt'
    # )

    model=YOLO(**config)

    if not os.path.exists(out_dir):os.makedirs(out_dir)
    for i,f in enumerate(glob.glob(imgs_dir+'/*.jpg')):
        img=Image.open(f)
        w,h=img.size
        r=1
        w=int(w*r)
        h=int(h*r)
        img=img.resize((w,h))
        rimg=model.detect_image(img)
        rimg.save(out_dir+'/'+os.path.basename(f))
        # rimg.show()
        # cv2.waitKey()
        # input()
        # os.system('killall display')

if __name__ == '__main__':
    demo()








