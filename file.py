import json
import os
from collections import OrderedDict

class files:
    def __init__(self,fname,mode="r"):
        filename=str(fname)+".json"
        if not os.path.isfile(filename):
            self.fptr=open(filename,"w")
            #self.fptr.write("{}")
            self.fptr.close()
        self.fptr=open(filename,mode)

    def fread(self,fname=""):
        self.fptr.seek(0,0)
        #self.data=json.loads(self.fptr.read())
        try:
            self.data = json.loads(self.fptr.read(), object_hook=OrderedDict)
        except ValueError:
            self.data = OrderedDict()
        return self.data

    def fwrite(self,matter,fname=""):
        data=self.fread()
        print (data)
        #print (matter)
        self.fptr.seek(0,0)
        data.update(matter)
        print (data)
        #self.fptr.seek(0,2)
        json.dump(data,self.fptr)

    def fclose(self):
        self.fptr.close()


x=files("table1","r+")
print (x.fread())
x.fwrite({2 : {"hi":1,"hello":2} })
#x.fwrite(OrderedDict([('hi1', 1), ('hello1', 2)]))
print (x.fread())
x.fclose()

        
        
