
class BatchList(list):
    def apply_(self,func,*args,**kwargs):
        for i,item in enumerate(self):
            self[i]=func(item,*args,**kwargs)
        # return self
    def apply(self,func,*args,**kwargs):
        lis=[func(item,*args,**kwargs) for item in self]
        return self.__class__(lis)

