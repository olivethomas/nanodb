import json
import os

class files:
    def __init__(self,fname,mode="r"):
        filename=str(fname)+".json"
        if not os.path.isfile(filename):
            self.fptr=open(filename,"w")
            self.fptr.write("{}")
            self.fptr.close()
        self.fptr=open(filename,mode)

    def fread(self,fname=""):
        self.fptr.seek(0,0)
        self.data=json.loads(self.fptr.read())
        return self.data

    def fwrite(self,matter,fname=""):
        self.fptr.seek(0,2)
        json.dump(matter,self.fptr)

    def fclose(self):
        self.fptr.close()


x=files("table1","r+")
print (x.fread())
x.fwrite({"hi":1,"hello":2})
print (x.fread())
x.fclose()

        
        
