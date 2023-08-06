import os,shutil,glob,json

class ObjectFile:
    def __init__(self,path,default=None):
        self.path=path
        if not os.path.exists(path):
            open(path,'w').close()
        if self.is_empty():
            self.write(default)
    def is_empty(self):
        with open(self.path) as f:
            s=f.read()
            if s=='':
                return True
        return False
    def __call__(self, obj=None):
        if obj is None:
            return self.read()
        return self.write(obj)
    def read(self):
        return json_load(self.path)
    def write(self,obj):
        return json_dump(obj, self.path)
class SimpleListFile(ObjectFile):
    def __init__(self,path,split_char='\n'):
        self.path=path
        self.split_char=split_char
        super().__init__(self.path,default=[])
    def write(self,obj):
        obj=self.split_char.join(obj)
        return writetxt(obj,self.path)
    def read(self):
        text=readtxt(self.path).strip()
        return text.split(self.split_char)
class DictFile(dict):
    def __init__(self,path):
        self.path=path
        if path.exists():
            assert os.path.isfile(path)
            dic=json_load(path)
            assert isinstance(dic,dict)
        else:
            dic={}
            open(path,'w').close()
            json_dump(dic,path,indent=4)
        super().__init__(dic)
    def __setattr__(self, key, value):
        dict.__setattr__(self,key,value)
        self._save()
    def __setitem__(self, key, value):
        dict.__setitem__(self,key,value)
        self._save()
    def update(self,*args,**kwargs):
        for k,v in kwargs.items():
            self[k]=v
        for arg in args:
            self.update(**arg)
    def _save(self):
        json_dump(self,self.path,indent=4)

class SimpleConfigFile(dict):
    def __init__(self,path,splitchar='=',comment_tag='#',sync=True):
        self.path=path
        self.splitchar=splitchar
        self.sync=sync
        super().__init__(read_config(path,splitchar=splitchar,comment_tag=comment_tag))
    def __setitem__(self, key, value):
        res=dict.__setitem__(self,key,value)
        if self.sync:
            self._save()
        return res
    def save(self):
        return self._save()
    def _save(self):
        return self.write()
    def write(self):
        write_config(self,self.path,splitchar=self.splitchar)

class NumberFile(ObjectFile):
    def __init__(self,path,default=0):
        super().__init__(path,default)


def dump_list_to_string(lis,template):
    if not template:
        return lis
    assert isinstance(template, (list, tuple, set))
    length = len(template)
    next_template = None
    if length == 1:
        cls=template[0]
        return str(lis)
    if length == 2:
        cls, splitchar = template
    else:
        cls, splitchar, next_template = template
    if cls in [list, set, tuple]:
        lis=list(lis)
        if next_template:
            for i,item in enumerate(lis):
                item = dump_list_to_string(item,next_template)
                lis[i]=item
        text = splitchar.join(lis)
        return text
    elif cls in [dict]:
        for k,v in lis.items():
            if next_template:
                v=dump_list_to_string(v,next_template)
            text=splitchar.join([k,v])
            return text

def dump_list_to_string_v2(lis,template):
    if not template:
        return lis
    assert isinstance(template, (list, tuple, set))
    length = len(template)
    next_template = None
    cls = template[0]
    if length == 1:
        return str(lis)
    else:
        if cls in [list, set, tuple]:
            lis=list(lis)
            assert length>=2
            splitchar=template[1]
            if length>=3:
                next_template=template[2]
            if next_template:
                for i,item in enumerate(lis):
                    item = dump_list_to_string(item,next_template)
                    lis[i]=item
            text = splitchar.join(lis)
            return text
        elif cls in [dict]:
            assert length>=3
            item_split=template[1]
            kv_split=template[2]
            items=[]
            for k,v in lis.items():
                if next_template:
                    v=dump_list_to_string(v,next_template)
                text=kv_split.join([k,v])
                items.append(text)
            text=item_split.join(items)
            return text

def load_list_from_string(text='',template=[list,'\n']):
    '''
    # [list,'\n',[dict,' ',[list,' ',[list,',']]]]
    '''
    if not template:
        return text
    assert isinstance(template, (list, tuple, set))
    length = len(template)
    next_template=None
    if length==1:
        cls=template[0]
        return cls(text)
    if length == 2:
        cls, splitchar = template
    else:
        cls, splitchar, next_template = template
    if cls in [list,set,tuple]:
        items=text.split(splitchar)
        if next_template:
            for i,item in enumerate(items):
                items[i]=load_list_from_string(item,next_template)
        items=cls(items)
        return items
    elif cls in [dict]:
        item={}
        k,v=text.split(splitchar,maxsplit=1)
        if next_template:
            v=load_list_from_string(v,next_template)
        item[k]=v
        return item

def load_list_from_string_v2(text='',template=[list,'\n']):
    '''
    # [list,'\n',[dict,' ',':',[list,' ',[list,',']]]]
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


def json_load(f,encoding='utf-8',*args,**kwargs):
    import json
    with open(f,'r',encoding=encoding) as fp:
        return json.load(fp,*args,**kwargs)
def json_dump(obj,fp,encoding='utf-8',*args,**kwargs):
    import json
    with open(fp,'w',encoding=encoding) as f:
        json.dump(obj,f,*args,**kwargs)
def readtxt(path,encoding='utf-8'):
    with open(path,'r',encoding=encoding) as f:
        return f.read()
def writetxt(txt,path,encoding='utf-8'):
    with open(path,'w',encoding=encoding) as f:
        f.write(txt)
def write_config(config,path,splitchar='='):
    open(path,'w').close()
    f=open(path,'a')
    for k,v in config.items():
        if isinstance(v,str):
            f.write('%s %s %s\n' % (key,splitchar,value))
        else:
            f.write('[%s]\n'%(k))
            assert isinstance(v,dict)
            for key,value in v.items():
                f.write('%s %s %s\n' % (key,splitchar,value))


def read_config(path,splitchar='=',comment_tag='#'):
    f=open(path,'r')
    config={}
    section_open=False
    current_section=None
    while True:
        s=f.readline()
        if not s:
            break
        if s.strip()=='':
            continue
        s=s.strip()
        if s.startswith('#'):
            continue
        if s.startswith('[') and s.endswith(']'):
            s=s[1:-1]
            assert '[' not in s and ']' not in s
            current_section=s
            config[current_section]={}
            section_open=True
            continue
        key,value=s.split(splitchar)
        key=key.strip()
        value=value.strip()
        if section_open:
            config[current_section][key]=value
        else:
            config[key]=value
    f.close()
    return config