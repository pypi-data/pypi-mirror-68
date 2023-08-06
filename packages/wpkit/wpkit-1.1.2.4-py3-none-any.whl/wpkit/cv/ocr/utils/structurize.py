import cv2
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image,ImageDraw
import re
import time,functools,math
import math
from . import trutils







class IterObject(dict):
    __no_value__='<__no_value__>'
    def __getattr__(self, key):
        v=self.get(key,self.__no_value__)
        if v is self.__no_value__:
            self[key]=IterObject()
            return self[key]
        else:
            return v
    def __setattr__(self, key, value):
        self[key]=value
class PointDict(dict):
    __no_value__='<__no_value__>'
    def __getattr__(self, key):
        return self.get(key)
    def __setattr__(self, key, value):
        self[key]=value
    def __call__(self, key , value=__no_value__):
        if value is self.__no_value__:
            self[key]=PointDict()
        else:
            self[key]=value
        return self[key]
    @classmethod
    def from_dict(cls,dic):
        dic2=cls()
        for k,v in dic.items():
            if not isinstance(v,dict):
                dic2[k]=v
            else:
                dic2[k]=cls.from_dict(v)
        return dic2
class TextBox(PointDict):
    def __init__(self,text,xywh,confidence=None):
        self.text=text
        x,y,w,h=xywh
        self.xywh=xywh
        self.ox,self.oy=x,y
        self.xmin,self.ymin=x,y
        self.xmax,self.ymax=x+w,y+h
        self.w, self.h = w, h
        self.cx,self.cy=x+w//2,y+h//2
        self.confidence=confidence
    def to_ltrb(self):
        return (self.xmin,self.ymin,self.xmax,self.ymax)
    def to_bbox(self):
        return (self.ox,self.oy,self.ox+self.w,self.oy+self.h)
    def match(self,patterns):
        for p in patterns:
            res=re.findall(p,self.text)
            if len(res):return res[0]
    @classmethod
    def from_tr_box(cls,k):
        return cls(k[1],k[0],k[2])
    @classmethod
    def from_ltrb(cls,box):
        b=box_utils.ltrb_to_xywh(box[0])
        return cls(box[1],b,box[2])
    @classmethod
    def union_two(cls,box1,box2):
        xmin=min(box1.xmin,box2.xmin)
        xmax=max(box1.xmax,box2.xmax)
        ymin=min(box1.ymin,box2.ymin)
        ymax=max(box1.ymax,box2.ymax)
        h=ymax-ymin
        w=xmax-xmin
        if box1.cx<box2.cx:
            text=box1.text+box2.text
        else:
            text=box1.text+box2.text
        confidence=min(box1.confidence,box2.confidence)
        newb=TextBox(text,(xmin,ymin,w,h),confidence)
        return newb

def sort_boxes(boxes,rx=1):
    if len(boxes)<=1:return boxes
    temp=sorted(boxes,key=lambda box:box['h'])
    mean_height=temp[len(boxes)//2]['h']
    temp=sorted(boxes,key=lambda box:box['cx'])
    left=temp[0]['cx']
    right=temp[-1]['cx']


    def map_x(x):
        x=(x-left)/(right-left)
        return x
    boxes=sorted(boxes,key=lambda box:box['cy']+rx*map_x(box['cx'])*mean_height)
    return boxes
class Framework(dict):
    def __init__(self, boxes, img_size=None,row_thresh=0.5,rx=0):
        boxes=[TextBox.from_tr_box(box) if not isinstance(box , TextBox) else box for box in boxes]
        boxes=self.remove_spaces(boxes)
        # boxes=sort_boxes(boxes)
        self.rows = self.orgnize_boxes(boxes,thresh=row_thresh,rx=rx)
        self.boxes = []
        k = 0
        for i, row in enumerate(self.rows):
            for j, box in enumerate(row):
                box['pos'] = (i, j)
                box['index'] = k
                self.rows[i][j] = box
                self.boxes.append(box)
                k += 1
            self[str(i)]=row
        self.cache = {}
        self.imsize = img_size
        self.fields={}
        self.res={}
        # print('*'*200)
        # self.print_rows()
    @classmethod
    def from_trboxes(cls,boxes):
        boxes=[TextBox.from_tr_box(box) for box in boxes]
        return cls(boxes)
    def replace_box_texts(self,replace_dict={}):
        if not replace_dict:
            return self
        default_dict={' ':'','\t':'','）':')','（':'(','：':':'}
        for box in self.boxes:
            box.text=self.replace_string(box.text,replace_dict)
        return self
    # def _replace_str(self,string,replace_dict={}):
    #     for k,v in replace_dict.items():
    #         string=string.replace(k,v)
    #     return string
    # def replace_all_str(self,replace_dict={}):
    #     if not replace_dict:
    #         return self
    #     for box in self.boxes:
    #         box['text']=self._replace_str(box['text'],replace_dict)
    #     return self
    def remove_spaces(self,boxes):
        for box in boxes:
            box.text=self.replace_string(box.text,{" ":"","\t":""})
        return boxes
    def _union_row(self,row,thresh=2):
        new_row=[row[0]]
        for i,box in enumerate(row[1:]):
            last=new_row[-1]
            if (box.xmin-last.xmax)<=(last.h*thresh):
                newb=TextBox.union_two(last,box)
                new_row[-1]=newb
                # print("find one:", last, box)
                # print("new box:",newb)
            else:
                new_row.append(box)
        return new_row

    def union_boxes_herizonal(self,thresh=2):
        boxes=[]
        for i,row in enumerate(self.rows):
            row=self._union_row(row,thresh)
            # print("row:",row)
            boxes+=row

        return Framework(boxes)

    def find_pattterns_in_string(self,ptns,text):
        for ptn in ptns:
            res=re.findall(ptn,text)
            if len(res):
                return res[0]
        return None
    def filter_nearest(self,box,boxes=None,n=1):
        boxes=boxes or self.boxes
        boxes=sorted(boxes,key=lambda bo:(bo['cx']-box['cx'])**2+(bo['cy']-box['cy'])**2)
        n=min(n,len(boxes))
        return boxes[:n]
    def find_field_in_one_box_else_most_likely_to_be_the_value_s2(self,loc_ptns,tar_ptns1,tar_ptns2,name,pre_str='',suf_str='',replace_dict={},nearest_n=1):
        box = self.find_box_by_str(patterns=loc_ptns)
        if box:
            res = self.find_field_in_this_box(box, ptns=tar_ptns1, name=name, pre_str=pre_str, suf_str=suf_str,
                                              replace_dict=replace_dict)
            if res:
                return res
            tmp_box = box
            # box = self.find_next_rightward(box)
            # if box:
            #     res = self.find_field_in_this_box(box, ptns=tar_ptns2, name=name, pre_str=pre_str, suf_str=suf_str,
            #                                       replace_dict=replace_dict)
            #     if res:
            #         return res
            nboxes = self.filter_nearest(tmp_box,boxes=self.filter_rightward(tmp_box,self.boxes), n=nearest_n)
            if len(nboxes):
                for nbox in nboxes:
                    box = nbox
                    res = self.find_field_in_this_box(box, ptns=tar_ptns2, name=name, pre_str=pre_str, suf_str=suf_str,
                                                      replace_dict=replace_dict)
                    if res:
                        return res
    # def find_field_in_one_box_else_most_likely_to_be_the_value_s2(self,loc_ptns,tar_ptns1,tar_ptns2,name,pre_str='',suf_str='',replace_dict={},nearest_n=3,ry=4):
    #     '''s2:style 2,different with original style'''
    #     box = self.find_box_by_str(patterns=loc_ptns)
    #     if box:
    #         res=self.find_field_in_this_box(box,ptns=tar_ptns1,name=name,pre_str=pre_str,suf_str=suf_str,replace_dict=replace_dict)
    #         if res:return res
    #         # boxes=self.filter_rightward(box)
    #         # # print('rightward boxes:',boxes)
    #         # bos = self.filter_vertical_nearest(box,boxes,nearest_n=nearest_n)
    #         bos=self.filter_most_likely_to_be_the_value_of_field(box,self.boxes,ry=ry,nearest_n=nearest_n)
    #         # print('box candidates:',bos)
    #         if bos:
    #             for bo in bos:
    #                 res = self.find_field_in_this_box(bo, ptns=tar_ptns2, name=name, pre_str=pre_str, suf_str=suf_str,
    #                                                   replace_dict=replace_dict)
    #                 if res:
    #                     return res
    def find_field_in_one_box_else_vertical_nearest_rightward_s2(self,loc_ptns,tar_ptns1,tar_ptns2,name,pre_str='',suf_str='',replace_dict={},nearest_n=3):
        '''s2:style 2,different with original style'''
        box = self.find_box_by_str(patterns=loc_ptns)
        if box:
            res=self.find_field_in_this_box(box,ptns=tar_ptns1,name=name,pre_str=pre_str,suf_str=suf_str,replace_dict=replace_dict)
            if res:return res
            boxes=self.filter_rightward(box)
            # print('rightward boxes:',boxes)
            bos = self.filter_vertical_nearest(box,boxes,nearest_n=nearest_n)
            if bos:
                for bo in bos:
                    res = self.find_field_in_this_box(bo, ptns=tar_ptns2, name=name, pre_str=pre_str, suf_str=suf_str,
                                                      replace_dict=replace_dict)
                    if res:
                        return res


    def find_field_in_vertical_nearest_rightward(self,loc_ptns,tar_ptns,name,pre_str='',suf_str='',replace_dict={}):
        box = self.find_box_by_str(patterns=loc_ptns)
        if box:
            bo=self.filter_vertical_nearest(box)
            if bo:
                bo=bo[0]
                res=self.find_field_in_this_box(bo,ptns=tar_ptns,name=name,pre_str=pre_str,suf_str=suf_str,replace_dict=replace_dict)
                if res:
                    return res

    def find_field_in_this_box(self,box,ptns,name,pre_str='',suf_str='',replace_dict={}):
        text = box.text
        text = self.replace_string(text, replace_dict)
        res = self.find_pattterns_in_string(ptns, text)
        if res:
            res = res.lstrip(pre_str).rstrip(suf_str)
            self.fields[name] = res
            return res
    def find_field_in_string(self,text,ptns,name,pre_str='',suf_str='',replace_dict={}):
        text = self.replace_string(text, replace_dict)
        res=self.find_pattterns_in_string(ptns,text)
        if res:
            res = res.lstrip(pre_str).rstrip(suf_str)
            self.fields[name] = res
            return res
    def find_field_in_one_box_else_next_v2(self,loc_ptns,tar_ptns1,tar_ptns2,name,pre_str='',suf_str='',replace_dict={}):
        box = self.find_box_by_str(patterns=loc_ptns)
        if box:
            res = self.find_field_in_this_box(box, ptns=tar_ptns1, name=name, pre_str=pre_str, suf_str=suf_str,
                                              replace_dict=replace_dict)
            if res:
                return res
            box2 = self.find_next_rightward(box)
            if box2:
                res = self.find_field_in_this_box(box2, ptns=tar_ptns2, name=name, pre_str=pre_str, suf_str=suf_str,
                                                  replace_dict=replace_dict)
                if res:
                    return res
    def find_field_in_one_box_else_next(self,loc_ptns,tar_ptns,name,pre_str='',suf_str='',replace_dict={},merge_row=False,extend_latter_boxes=False):

        box=self.find_box_by_str(patterns=loc_ptns)
        if box:
            if extend_latter_boxes:
                # box = self.find_box_by_str(patterns=loc_ptns)
                #
                boxes = self.get_following_boxes_in_row(box)
                text = self.connect_boxes_texts(boxes)
                res = self.find_field_in_string(text, ptns=tar_ptns, name=name, pre_str=pre_str, suf_str=suf_str,
                                                replace_dict=replace_dict)
                if res:
                    return res
            res=self.find_field_in_this_box(box,ptns=tar_ptns,name=name,pre_str=pre_str,suf_str=suf_str,replace_dict=replace_dict)
            if res:
                return res
            box2=self.find_next_rightward(box)
            if box2:
                res = self.find_field_in_this_box(box2, ptns=tar_ptns, name=name, pre_str=pre_str, suf_str=suf_str, replace_dict=replace_dict)
                if res:
                    return res
            if merge_row:
                row = self.get_row(box)
                text = self.connect_boxes_texts(row)
                text = self.replace_string(text, replace_dict)
                res = self.find_pattterns_in_string(ptns=tar_ptns, text=text)
                if res:
                    res = res.lstrip(pre_str).rstrip(suf_str)
                    self.fields[name] = res
                    return res
    def find_field_here_next_nearest_anywhere(self,loc_ptns,tar_ptns,name,pre_str='',suf_str='',replace_dict={}):
        res=self.find_field_in_one_box_else_next_else_nearest(loc_ptns=loc_ptns,tar_ptns=tar_ptns,name=name,pre_str=pre_str,suf_str=suf_str,replace_dict=replace_dict)
        if res:
            return res
        res=self.find_this_field(ptns=tar_ptns,name=name,pre_str=pre_str,suf_str=suf_str,replace_dict=replace_dict)
        if res:
            return res

    def find_field_in_one_box_else_next_else_nearest(self,loc_ptns,tar_ptns,name,pre_str='',suf_str='',replace_dict={},nearest_n=1):
        box = self.find_box_by_str(patterns=loc_ptns)
        if box:
            res = self.find_field_in_this_box(box, ptns=tar_ptns, name=name, pre_str=pre_str, suf_str=suf_str,
                                              replace_dict=replace_dict)
            if res:
                return res
            tmp_box=box
            box = self.find_next_rightward(box)
            if box:
                res = self.find_field_in_this_box(box, ptns=tar_ptns, name=name, pre_str=pre_str, suf_str=suf_str,
                                                  replace_dict=replace_dict)
                if res:
                    return res
            nboxes=self.nearest_boxes(tmp_box,n=nearest_n)
            if len(nboxes):
                for nbox in nboxes:
                    box = nbox
                    res = self.find_field_in_this_box(box, ptns=tar_ptns, name=name, pre_str=pre_str, suf_str=suf_str,
                                                      replace_dict=replace_dict)
                    if res:
                        return res
            # nbox=self.find_nearest_box(box)
            #
            # if nbox!=box:
            #     box=nbox
            #     res = self.find_field_in_this_box(box, ptns=tar_ptns, name=name, pre_str=pre_str, suf_str=suf_str,
            #                                       replace_dict=replace_dict)
            #     if res:
            #         return res
    def find_field_in_one_box_else_next_else_nearest_s2(self,loc_ptns,tar_ptns1,tar_ptns2,name,pre_str='',suf_str='',replace_dict={},nearest_n=1):
        box = self.find_box_by_str(patterns=loc_ptns)
        if box:
            res = self.find_field_in_this_box(box, ptns=tar_ptns1, name=name, pre_str=pre_str, suf_str=suf_str,
                                              replace_dict=replace_dict)
            if res:
                return res
            tmp_box=box
            box = self.find_next_rightward(box)
            if box:
                res = self.find_field_in_this_box(box, ptns=tar_ptns2, name=name, pre_str=pre_str, suf_str=suf_str,
                                                  replace_dict=replace_dict)
                if res:
                    return res
            nboxes=self.nearest_boxes(tmp_box,n=nearest_n)
            if len(nboxes):
                for nbox in nboxes:
                    box = nbox
                    res = self.find_field_in_this_box(box, ptns=tar_ptns2, name=name, pre_str=pre_str, suf_str=suf_str,
                                                      replace_dict=replace_dict)
                    if res:
                        return res
            # nbox=self.find_nearest_box(box)
            #
            # if nbox!=box:
            #     box=nbox
            #     res = self.find_field_in_this_box(box, ptns=tar_ptns, name=name, pre_str=pre_str, suf_str=suf_str,
            #                                       replace_dict=replace_dict)
            #     if res:
            #         return res

    def find_this_field(self,ptns,name,*args,**kwargs):
        self.find_field_in_one_box(loc_ptns=ptns,tar_ptns=ptns,name=name,*args,**kwargs)
    def find_simple_field(self,patterns,name,replace_dict={" ":""},tar_ptns=None):
        box=self.find_box_by_str(patterns=patterns,replace_dict=replace_dict)
        if box:
            b=self.find_next_rightward(box)
            # print(box,b)
            if b:
                text=b.text
                if not tar_ptns:
                    self.fields[name]=text
                    return text
                else:
                    text = self.find_pattterns_in_string(tar_ptns,text)
                    if text:
                        self.fields[name]=text
                        return text
    def find_field_in_one_box(self,loc_ptns,tar_ptns,name,pre_str='',suf_str='',replace_dict={}):
        box = self.find_box_by_str(patterns=loc_ptns)
        if box:
            text=box.text
            text=self.replace_string(text,replace_dict)
            for ptn in tar_ptns:
                r=re.findall(ptn,text)
                if r:
                    res=r[0]
                    res=res.lstrip(pre_str).rstrip(suf_str)
                    self.fields[name]=res
                    return res
    def __getitem__(self, *args):
        if isinstance(args[0],slice):# len=1
            sl1=args[0]
            return self.rows[sl1]
        else:#len>1
            res=self.rows
            for i in range(len(args[0])):
                sl=args[0][i]
                res=res[sl]
            return res
    def get_row(self,box):
        return self.rows[box.pos[0]]
    def get_last_row(self,box):
        r=box.pos[0]
        return self.rows[r-1] if r else None
    def get_next_row(self,box):
        r=box.pos[0]
        return self.rows[r+1] if not r==len(self.rows)-1 else None
    def get_following_boxes_in_row(self,box):
        return [box]+self.get_row(box)[box.pos[1]+1:]
    def nearest_boxes(self,box,n=-1):
        newboxes = self.boxes.copy()
        newboxes.remove(box) if box in newboxes else None
        if not len(newboxes):return []
        newboxes.sort(key=lambda b: (b.cx - box.cx) ** 2 + (b.cy - box.cy) ** 2)
        if n<0:
            n=len(newboxes)
        else:
            n=min(n,len(newboxes))
        return newboxes[:n]
    def find_nearest_box(self,box):
        newboxes=self.boxes.copy()
        newboxes.remove(box)
        newboxes.sort(key=lambda b:(b.cx-box.cx)**2+(b.cy-box.cy)**2)
        return newboxes[-1]
    def next_box_in_same_row(self,box):
        m,n=box.pos
        row=self.rows[m]
        if n>=len(row)-1:
            return None
        return row[n+1]
    def find_next_n(self, box, k):
        m, n = box['pos']
        boxes = []
        num = 0
        end = False
        for i, row in enumerate(self.rows[m:]):
            if end:
                break
            for j, box in enumerate(row[n:]):
                boxes.append(box)
                num += 1
                if num == k + 1:
                    end = True
                    break
        boxes = boxes[1:]
        return boxes
    def find_index(self,box):
        cx, cy ,w,h= box['cx'], box['cy'],box['w'],box['h']
        for b in self.boxes:
            if b['cx'] == cx and b['cy'] == cy and b['w']==w and b['h']==h:
                return b['index']
    def find_pos(self, box):
        cx, cy, w, h = box['cx'], box['cy'], box['w'], box['h']
        for b in self.boxes:
            if b['cx'] == cx and b['cy'] == cy and b['w'] == w and b['h'] == h:
                return b['pos']
    def _filter(self,box,boxes=None,key=None,preprocess=None):
        boxes = boxes or self.boxes
        if not key:return boxes
        # assert hasattr(key,'__call__')
        if preprocess:
            boxes=preprocess(boxes)
        boxset=[]
        for i,bo in enumerate(boxset):
            if key(bo,box,i,boxes,boxset):
                boxset.append(bo)
        return boxset
    def filter_rightward(self,box,boxes=None,min_dist=0,max_dist=math.inf,refer='right'):
        # def key(bo,box,*args,**kwargs):
        #     if refer=='right':
        #         dist=bo['cx']-box['xmax']
        #     else:
        #         raise NotImplementedError
        #     if dist>min_dist and dist<max_dist:
        #         return True
        #     else:
        #         return False
        # boxes=self._filter(box,boxes,key=key)
        boxset=[]
        for bo in self.boxes:
            if bo['cx']-box['xmax']>0:
                boxset.append(bo)
        return boxset
    def filter_most_likely_to_be_the_value_of_field(self,box,boxes=None,ry=4,nearest_n=1):
        boxes=boxes or self.boxes
        boxes=list(filter(lambda bo:bo['cx']>box['xmax'],boxes))
        # boxes=sorted(boxes,key=lambda bo:ry*abs(bo['cy']-box['cy'])+abs(bo['cx']-box['xmax']))
        boxes=sorted(boxes,key=lambda bo:abs(bo['cy']-box['cy'])**2+abs(bo['cx']-box['xmax'])**2)
        num=min(nearest_n,len(boxes))
        return boxes[:num]

        # for i, bo in enumerate(boxes):

    def filter_vertical_nearest(self,box,boxes=None,max_dist=math.inf,nearest_n=1):
        boxes=boxes or self.boxes
        boxes=list(filter(lambda bo:(abs(bo['cy']-box['cy'])<=max_dist) and bo['index']!=box['index'],boxes))
        boxes=sorted(boxes,key=lambda bo:abs(bo['cy']-box['cy']))
        num=min(nearest_n,len(boxes))
        return boxes[:num]






    def find_next_rightward(self,box):
        index=self.find_index(box)
        m,n=box['pos']
        if index==len(self.boxes)-1:
            return None
        if n>=len(self.rows[m]):
            return None
        return self.boxes[index+1]

    def find_next_downward(self, box):
        m, n = self.find_pos(box)
        if m >= len(self.rows):
            return None
        cands = self.rows[m + 1]
        cands = sorted(cands, key=lambda b: (b['cx'] - box['cx']) ** 2 + (b['cy'] - box['cy']) ** 2)
        return cands[0]

    def union_boxes(self,boxes,split_char=''):
        assert len(boxes)

        b=boxes[0]
        xmin,ymin,xmax,ymax=b.ox,b.oy,b.ox+b.w,b.oy+b.h
        text = b.text
        confidence=b.confidence
        for b in boxes[1:]:
            text+=split_char+b.text
            xmin=min(xmin,b.ox)
            ymin=min(ymin,b.oy)
            xmax=max(xmax,b.ox+b.w)
            ymax=max(ymax,b.oy+b.h)
            confidence=min(confidence,b.confidence)
        x=xmin
        y=ymin
        w=xmax-xmin
        h=ymax-ymin
        newb=TextBox(text,(x,y,w,h),confidence=confidence)
        return newb


    def connect_vertical_downward(self, box,try_hard=True):
        def is_vertically_adjacent(b1, b2):
            # print('b1,b2:',b1,b2)
            ro = 0.2  # 横向超出占行宽的最大比重
            rv = 3  # 纵向距离占行高的最大比重
            if b2['cx'] > b1['xmax'] or b2['cx'] < b1['xmin']: return False
            if b2['cy'] < b1['cy'] or (b2['cy'] - b1['cy']) > b1['h'] * rv: return False

            ofl = b1['xmin'] - b2['xmin'] if b2['xmin'] < b1['xmin'] else 0
            ofr = b2['xmax'] - b1['xmax'] if b2['xmax'] > b1['xmax'] else 0
            off = ofl + ofr
            if off > ro * b1['w']: return False
            return True

        if try_hard:
            m,n=box.pos
            ind=box.index
            boxset=[box]
            for b in self.boxes[ind+1:]:
                if is_vertically_adjacent(boxset[-1],b):
                    boxset.append(b)
            return boxset

        box['pos'] = self.find_pos(box)
        m, n = box['pos']
        boxset = []


        for row in self.rows[m:]:
            # print('row:',row)
            for b in row[n:]:
                if len(boxset) == 0:
                    boxset.append(b)
                    continue
                if is_vertically_adjacent(boxset[-1], b): boxset.append(b)
        self.cache['boxset']=boxset
        return boxset

    def orgnize_boxes(self,boxes,try_harder=False,thresh=0.5,rx=0):
        rows = []
        # boxes.sort(key=lambda box: int(box['cy']))
        boxes=sort_boxes(boxes,rx=rx)
        for box in boxes:
            if len(rows) == 0:
                row = [box]
                rows.append(row)
                continue
            #     quick version
            last_box = rows[-1][-1]
            if box['cy'] <= last_box['cy'] + int(last_box['h'] * thresh):
            #     slow version
            # if self.is_box_in_row_slowly(box,rows[-1]):
            # if self.is_the_next_box_in_row(box,rows[-1]):
                if try_harder:
                    if self.is_box_in_row_using_angle(box,rows[-1]):
                        rows[-1].append(box)
                        # print('box in rows:',box,len(rows)-1)
                else:
                    rows[-1].append(box)
            else:
                row = [box]
                rows.append(row)
        for row in rows:
            row.sort(key=lambda box: int(box['cx']))
        # print('boxes:', rows)
        # print('*' * 100)
        return rows

    def find_boxes(self, key, boxes=None):
        boxes = self.boxes if not boxes else boxes
        boxset = []
        [boxset.append(box) if key(box) else None for box in boxes]
        return boxset

    def in_area(self, box, xr=None, yr=None):
        assert self.imsize is not None
        h, w = self.imsize
        cx, cy = box['cx'], box['cy']
        if xr and not (cx >= xr[0] * w and cx <= xr[1] * w):
            return False
        if yr and not (cy >= yr[0] * h and cy <= yr[1] * h):
            return False
        return True
    def replace_string(self,s,dic):

        for k,v in dic.items():
            s=s.replace(k,v)
        return s
    def __find_box_by_str(self, boxes, pattern,replace_dict={}):
        import re
        boxes2 = []
        for box in boxes:
            text=box['text']
            text=self.replace_string(text,replace_dict)
            res = re.findall(pattern, text)
            if len(res) != 0:
                boxes2.append(box)
        return boxes2
    def find_str_in_boxes(self,patterns,boxes=None):
        boxes = boxes or self.boxes
        for pattern in patterns:
            for box in boxes:
                res=re.findall(pattern,box.text)
                if res and len(res):
                    return res[0]
    def find_box_by_str(self, patterns,boxes=None,replace_dict={" ":''}):
        boxes=boxes or self.boxes
        for pattern in patterns:
            boxset = self.__find_box_by_str(boxes, pattern,replace_dict=replace_dict)
            if len(boxset):
                return boxset[0]
    def find_boxes_by_str(self, patterns,boxes=None,replace_dict={" ":''}):
        boxes=boxes or self.boxes
        for pattern in patterns:
            boxset = self.__find_box_by_str(boxes, pattern,replace_dict=replace_dict)
            if len(boxset):
                return boxset
    def print_rows(self,full_info=False,info_keys=None):
        if not full_info:
            info_keys=info_keys or ['text','confidence']
            for row in self.rows:
                new_row=[{k:box[k] for k in info_keys} for box in row]
                print(new_row)
            return
        for row in self.rows:
            print(row)
    def connect_boxes_texts(self,boxes):
        text=''
        for b in boxes:
            text+=b.text
        return text

    #############################################
    # Tools for orgnizing boxes
    def is_box_in_row_using_angle(self,box,row):
        for b in row:
            if not self.is_two_box_in_same_row_using_angle(b,box):return False
        return True
    def is_two_box_in_same_row_using_angle(self,box1,box2):
        import math
        dx=abs(box1['cx']-box2['cx'])
        dy=abs(box1['cy']-box2['cy'])
        if not dx:return False
        ang=math.atan2(dy,dx)*180/math.pi
        yes=ang<45
        if yes:
            # print('dx,dy:',dx,dy)
            print('angle:%s , boxes: %s , %s'%(ang,box1.text,box2.text))
        return yes
    def is_the_next_box_in_row(self,box,row):
        '''先看横坐标是否匹配，进一步检查两个box纵向重合区间占比'''
        box1=row[-1]
        box2=box
        if box2['cx']<box1['cx']:
            return False
        l1, t1, r1, b1 = box1.to_bbox()
        l2, t2, r2, b2 = box2.to_bbox()

        def get_intersection_length(rg1, rg2):
            if rg1[1] <= rg2[0] or rg1[0] >= rg2[1]:
                return False
            elif rg1[1] < rg2[1]:
                return rg1[1] - rg2[0]
            elif rg1[0] < rg2[0]:
                return rg2[1] - rg2[0]
            else:
                return rg2[1] - rg1[0]

        h1, h2 = box1['h'], box2['h']
        cy1, cy2 = box1['cy'], box2['cy']
        m = get_intersection_length([t1, b1], [t2, b2])
        if not m: return False
        rm = max(m / h1, m / h2)
        yes=rm > 0.4
        if yes:
            print('%scheck1: same row :%s , %s'%('`'*80,box1.text,box2.text))
        return yes
    def is_two_box_in_same_row(self,box1,box2):
        '''根据两个box纵向重合的区间长度来判断,效果不好，没有考虑x坐标的大小信息'''
        l1,t1,r1,b1=box1.to_bbox()
        l2,t2,r2,b2=box2.to_bbox()
        def get_intersection_length(rg1,rg2):
            if rg1[1]<=rg2[0] or rg1[0]>=rg2[1]:return False
            elif rg1[1]<rg2[1]:return rg1[1]-rg2[0]
            elif rg1[0]<rg2[0]:return rg2[1]-rg2[0]
            else:return rg2[1]-rg1[0]
        h1,h2=box1['h'],box2['h']
        cy1,cy2=box1['cy'],box2['cy']
        m=get_intersection_length([t1,b1],[t2,b2])
        if not m:return False
        rm=max(m/h1,m/h2)
        return rm >0.4

    def is_box_in_row_slowly(self,box,row):
        '''与横向最近的一个box相比，判断纵向坐标匹配'''
        assert len(row)
        row2=row
        row2.sort(key=lambda b:abs(box['cx']-b['cx']))
        b=row2[-1]
        if box['cy']<=b['cy']+int(b['h']*0.5):
            return True
        return False


class Timer:
    def __init__(self, verbose=True,msg=None,mute=None):
        self.history = []
        self.dt_history = []
        self.steps = 0
        self.start_time = time.time()
        self.history.append(self.start_time)
        self.verbose = verbose
        self.mute=mute
        if self.verbose:
            self.tprint('Timer started at %s' % (self.start_time))
        if msg:
            self.tprint(msg)
    def tprint(self,*args,**kwargs):
        if not self.mute:
            print(*args)
    def step(self,msg=None):
        t = time.time()
        dt = t - self.history[-1]
        self.dt_history.append(dt)
        self.history.append(t)
        self.steps += 1
        if self.verbose:
            self.tprint('step=%s , %s time since last step: %s' % (self.steps,'msg=%s,'%(msg) if msg else '',dt))
        return dt
    def mean(self):
        if not len(self.dt_history):return None
        return sum(self.dt_history)/len(self.dt_history)
    def plot_dt_history(self,title='Timer History',*args,**kwargs):
        from matplotlib import pyplot as plt
        plt.plot(self.dt_history)
        plt.show(title=title,*args,**kwargs)

    def end(self):
        t = time.time()
        self.end_time = t
        dt = t - self.history[-1]
        self.dt_history.append(dt)
        self.history.append(t)
        self.steps += 1
        if self.verbose:
            self.tprint('time since last step: %s' % (dt))
        return dt

def run_timer(func):
    name = func.__name__

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print('running %s ...' % (name))
        t = Timer(verbose=False)
        ret = func(*args, **kwargs)
        dt = t.end()
        print('finished running %s ,time consumed: %s' % (name, dt))
        return ret
    return wrapper

def test_speed(func,times=10):
    T=Timer()
    for i in range(times):
        func()
        T.step()
    print('Mean time:',T.mean())