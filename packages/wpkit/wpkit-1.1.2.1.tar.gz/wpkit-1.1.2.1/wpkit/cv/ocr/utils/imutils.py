import numpy as np
import cv2
from PIL import Image,ImageDraw,ImageFont
from matplotlib import pyplot as plt
def pilimg(img):
    if isinstance(img,Image.Image):
        return img
    if isinstance(img,str):
        img=Image.open(img)
    elif not isinstance(img,Image.Image):
        img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        img=Image.fromarray(img)
    return img
def cv2img(img):
    if isinstance(img,str):
        img=cv2.imread(img)
    elif isinstance(img,Image.Image):
        img=np.array(img).astype(np.uint8)
        img=cv2.cvtColor(img,cv2.COLOR_RGB2BGR)
    return img
def crop_quad(img,box):
    p0, p1, p2, p3 = box
    (x0, y0), (x1, y1), (x2, y2), (x3, y3) = box
    w,h=((x1-x0+x2-x3)//2,(y3-y0+y2-y1)//2)
    w,h=int(w),int(h)
    M=cv2.getPerspectiveTransform(np.float32([p0,p1,p3,p2]),np.float32([[0,0],[w,0],[0,h],[w,h]]))
    # print(img,M,w,h)
    img=cv2.warpPerspective(img,M,(w,h))
    return img
def crop_quads(img,boxes):
    bims=[]
    for box in boxes:
        bims.append(crop_quad(img,box))
    return bims


def order_points_old(pts):
    # 初始化坐标点
    rect = np.zeros((4, 2), dtype="float32")

    # 获取左上角和右下角坐标点
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]

    # 分别计算左上角和右下角的离散差值
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]

    return rect
def order_points(pts):
    # 初始化坐标点
    rect = np.zeros((4, 2), dtype="float32")

    # 获取左上角和右下角坐标点
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]

    # 分别计算左上角和右下角的离散差值
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]

    return rect


def four_point_transform(image, pts):
    '''
    顺时针
    :param image:
    :param pts: (tl, tr, br, bl)
    :return:
    '''
    # 获取坐标点，并将它们分离开来
    pts=np.array(list(pts))
    rect = order_points(pts)
    # pts=[list(item) for item in pts]
    # print("ptns:",pts)
    # rect=np.array(pts,dtype=np.float32)
    (tl, tr, br, bl) = rect

    # 计算新图片的宽度值，选取水平差值的最大值
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))

    # 计算新图片的高度值，选取垂直差值的最大值
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))

    # 构建新图片的4个坐标点
    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype="float32")

    # 获取仿射变换矩阵并应用它

    M = cv2.getPerspectiveTransform(rect, dst)
    # 进行仿射变换
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))

    # 返回变换后的结果
    return warped


def blank_rgb_img(size,color='white'):
    img = Image.new('RGB', size=size, color=color)
    return img
def new_blank_img_as(img):
    img=Image.new('RGB',size=img.size,color='white')
    return img
def pilimshow(x,*args,**kwargs):
    x=pilimg(x)
    x.show(*args,**kwargs)
def cv2imshow(x,title='cv2 image'):
    x=cv2img(x)
    cv2.imshow(title,x)
    cv2.waitKey(0)
def pltimshow(x,*args,**kwargs):
    x=cv2img(x)
    plt.imshow(x,*args,**kwargs)
    plt.show()
def resize_to_fixed_height(img,height):
    w,h=img.size
    r=h/height
    nw=int(w/r)
    nh=int(h/r)
    img=img.resize((nw,nh))
    return img
def resize_to_fixed_width(img,width):
    w,h=img.size
    r=w/width
    nw=int(w/r)
    nh=int(h/r)
    img=img.resize((nw,nh))
    return img
def resize_by_scale(img,scale):
    w, h = img.size
    r = scale
    nw = int(w * r)
    nh = int(h * r)
    img = img.resize((nw, nh))
    return img
def limit_size(img,limits):
    w,h=img.size
    mw,mh=limits
    rw=w/mw
    rh=h/mh
    r=max(rw,rh)
    if r<=1:
        return img
    nw=int(w/r)
    nh=int(h/r)
    img=img.resize((nw,nh))
    return img
def draw_boxes(img,boxes,copy=False,*args,**kwargs):
    if copy:
        img=img.copy()
    for box in boxes:img=draw_box(img,box,copy=False,*args,**kwargs)
    return img
def draw_box(img,box,copy=True,width=5,outline='red',fill=None):
    box=tuple(box)
    if copy:
        img=img.copy()
    draw=ImageDraw.Draw(img)
    draw.rectangle((box[:2],box[2:]),width=width,outline=outline,fill=fill)
    return img
def draw_textboxes(img,textboxes,copy=False,font_size=32):
    if copy:
        img=img.copy()
    for textbox in textboxes:
        img=draw_textbox(img,textbox,copy=False,font_size=font_size)
    return img

def draw_textbox(img,textbox,copy=True,font_size=None):
    '''

    :param img:
    :param textbox:((l,t,r,b),text)
    :param copy:
    :param font_size:
    :return:
    '''
    import os
    font_size=font_size or 32
    box,text=textbox
    if copy:
        img=img.copy()
    draw = ImageDraw.Draw(img)
    font=ImageFont.truetype(os.path.dirname(__file__)+'/msyh.ttf',size=font_size)
    draw.text(box[:2],text=text,fill='black',font=font)
    return img
def crop_boxes(img,boxes):
    imgs=[]
    for box in boxes:
        im=crop(img,box)
        imgs.append(im)
    return imgs
def iter_boxes(img,boxes,do):
    reses=[]
    for box in boxes:
        im=crop(img,box)
        res=do(im)
        reses.append(res)
    return reses
def crop(img,bbox):
    return img.crop(bbox)
def crop_by_ratio(img,rbox):
    w,h=img.size
    box=tuple([int(x) for x in (rbox[0]*w,rbox[1]*h,rbox[2]*w,rbox[3]*h)])
    return img.crop(box)