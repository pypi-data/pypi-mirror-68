import cv2
from PIL import Image
import numpy as np
import math,os,shutil,glob,random,json,time
from .abstract import BatchList
from . import boxutils as BU
from . import imutils as IU

class BoxBatch(BatchList):
    def mean(self):
        if not len(self):return None
        return sum(self)/(len(self))
    def angle(self):
        return self.apply(BU.angle)
    def organize_points(self):
        return self.apply(BU.organize_points)
    def numpy(self):
        return np.array(self)
class TextBox(dict):
    def __init__(self):
        super().__init__()
    def parse(self):
        p0,p1,p2,p3=quad=self['quad']
        xmin,ymin,xmax,ymax=l,t,r,b=ltrb=BU.quad_to_ltrb(quad)
        ox,oy,w,h=oowh=BU.ltrb_to_oowh(ltrb)
        cx,cy,w,h=ccwh=BU.ltrb_to_ccwh(ltrb)
        angle=BU.angle(quad)
        text=None
        prob=None
        self.update(
            ltrb=ltrb,oowh=oowh,ccwh=ccwh,
            xmin=xmin,ymin=ymin,xmax=xmax,ymax=ymax,
            l=l,t=t,r=r,b=b,
            ox=ox,oy=oy,w=w,h=h,
            cx=cx,cy=cy,
            angle=angle,
            text=text,
            prob=prob
        )
        return self