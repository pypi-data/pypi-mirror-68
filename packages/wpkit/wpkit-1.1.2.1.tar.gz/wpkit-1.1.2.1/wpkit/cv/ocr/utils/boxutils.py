import cv2
from PIL import Image
import numpy as np
import math,os,shutil,glob,random,json,time
from .abstract import BatchList



def pad_box(box,pad_size=5,pad_ratio=None,max_w=None,max_h=None):
    from math import inf
    w=max_w or inf
    h=max_h or inf
    l,t,r,b=box
    bh=b-t
    bw=r-l
    if pad_ratio is not None:
        if isinstance(pad_ratio,(tuple,list)):
            if len(pad_ratio)==2:
                pad_l=pad_r=int(min(bh,bw)*pad_ratio[0])
                pad_t=pad_b=int(min(bh,bw)*pad_ratio[1])
            else:
                assert len(pad_ratio)==4
                pad_l= int(min(bh, bw) * pad_ratio[0])
                pad_t= int(min(bh, bw) * pad_ratio[1])
                pad_r= int(min(bh, bw) * pad_ratio[2])
                pad_b= int(min(bh, bw) * pad_ratio[3])
        else:
            pad_l=pad_t=pad_r=pad_b=int(min(bh,bw)*pad_ratio)
    else:
        if isinstance(pad_size,(tuple,list)):
            if len(pad_size)==2:
                pad_l=pad_r=pad_size[0]
                pad_t=pad_b=pad_size[1]
            else:
                assert len(pad_size)==4
                pad_l,pad_t,pad_r,pad_b=pad_size
        else:
            pad_l=pad_t=pad_r=pad_b=pad_size
    l=max(0,l-pad_l)
    t=max(0,t-pad_t)
    r=min(w,r+pad_r)
    b=min(h,b+pad_b)
    return box.__class__([l,t,r,b])

def resize_box(box, size):
    cx, cy, w, h = ltrb_to_ccwh(box)
    nw, nh = size
    l = cx - nw // 2
    r = cx + nw // 2
    t = cy - nh // 2
    b = cy + nh // 2
    return box.__class__([l, t, r, b])

def limit_box(box, limits):
    if len(limits) == 2:
        ml, mt = 0, 0
        mr, mb = limits
    else:
        assert len(limits) == 4
        ml, mt, mr, mb = limits
    l, t, r, b = box
    l = max(ml, l)
    t = max(mt, t)
    r = min(mr, r)
    b = min(mb, b)
    if l >= r:
        return None
    if t >= b: return None
    return box.__class__([l, t, r, b])

def ltrb_to_ccwh(box):
    '''c:center'''
    l, t, r, b = box
    w = r - l
    h = b - t
    cx = (l + r) // 2
    cy = (t + b) // 2
    return box.__class__([cx, cy, w, h])

def ccwh_to_ltrb(box):
    cx, cy, w, h = box
    l = cx - w // 2
    t = cy - h // 2
    r = cx + w // 2
    b = cy + h // 2
    return box.__class__([l, t, r, b])

def oowh_to_ltrb(box):
    '''o:origin'''
    x, y, w, h = box
    return box.__class__([int(i) for i in (x, y, x + w, y + h)])

def ltrb_to_oowh(box):
    l, t, r, b = box
    return box.__class__([l, t, r - l, b - t])

def quad_to_ltrb(box):
    (x0,y0),(x1,y1),(x2,y2),(x3,y3)=box
    return box.__class__([min(x0,x3),min(y0,y1),max(x1,x2),max(y2,y3)])

def minAreaRect(box):
    return quad_to_ltrb(box)

def organize_points(box):
    '''
    turn into clock-wise points
    p0:lt,p1:rt,p2:rb,p4:lb
    '''
    p0,p3, p1,p2 = sorted(box, key=lambda p: p[0])
    p03=[p0,p3]
    p12=[p1,p2]
    p0, p3 = sorted(p03, key=lambda p: p[1])
    p1, p2 = sorted(p12, key=lambda p: p[1])
    return box.__class__([p0,p1,p2,p3])

def angle(quad):
    '''cal angle of a quad'''
    p0,p1,p2,p3=quad
    def center(p1,p2):
        x1,y1=p1
        x2,y2=p2
        return (x1+x2)/2,(y1+y2)/2
    x1,y1=center(p0,p3)
    x2,y2=center(p1,p2)
    angle=math.atan2(y1-y2,x2-x1)*180/math.pi
    # print(p0, p1, p2, p3, (x1, y1), (x2, y2), angle)
    return angle



