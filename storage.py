import json
import os
from collections import OrderedDict

class Storage:
    def __init__(self,fname):
        self.fptr=None
        filename=str(fname)+".json"
        if os.path.isfile(filename):
            self.fptr=open(filename,"r+")
            self.fptr.close()
               
         
            
    def fcreate(self,fname,mode="r"):
        filename=str(fname)+".json"
        if not os.path.isfile(filename):
            self.fptr=open(filename,"w")
            #self.fptr.write("{}")
            self.fptr.close()
        #self.fptr=open(filename,mode)
        

    def fopen(self,fname,mode="r"):
        filename=str(fname)+".json"
        if not os.path.isfile(filename):
            return 0
        else:
            self.fptr=open(filename,mode)
            return 1

    def fread(self,fname):
        if self.fopen(fname)==0:
            return -1
        self.fptr.seek(0,0)
        #self.data=json.loads(self.fptr.read())
        try:
            self.data = json.loads(self.fptr.read())
        except ValueError:
            self.data ={}
        self.fclose()
        return self.data

    def fwrite(self,matter,fname,mode="r+"):
        data=self.fread(fname)
        if self.fopen(fname,mode)==0:
            return
        self.fptr.seek(0,0)
        data.update(matter)
        #print (data)
        #self.fptr.seek(0,2)
        json.dump(data,self.fptr)
        self.fclose()

    def fclose(self):
        self.fptr.close()


#x=storage("table1","r+")
#print (x.fread("table1"))
#x.fwrite({3 : {"hi":1,"hello":2} }, "table1")
#x.fwrite(OrderedDict([('hi1', 1), ('hello1', 2)]))
#print (x.fread("table1"))
#x.fclose()

        
        
