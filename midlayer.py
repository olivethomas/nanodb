import json
from storage import Storage 
class Midlayer:
  
    def __init__(self):
        self.file_obj=None
        self.id=0
        
    def opendb(self,db_name):
        self.file_obj=Storage(db_name)
        if self.file_obj.fptr is None:
            return 0
        return 1
            
    def create(self,db_name):
        self.file_obj=Storage(db_name)
        if self.file_obj.fcreate(db_name):
            self.insert(db_name,{"lastid": 0})
            return 1
        return 0

    def view_records(self,db_name):
        if self.opendb(db_name):
            data=self.file_obj.fread(db_name)
            #print (data)
            return data
    
    def find_numberof_records(self,db_name):
        if self.opendb(db_name):
            data=self.file_obj.fread(db_name)
            length=len(data)
            return length
        
    
    def insert(self,db_name,data):
        self.id=self.find_numberof_records(db_name)
        if self.id is not None:
            if self.id!=0:
                metadata = self.file_obj.fgetmetadata(db_name)
                print (self.id,metadata)
                self.id=metadata["lastid"]+1
            record={}
            record[self.id]=data
            record["0"]={}
            record["0"]["lastid"]=self.id
            self.file_obj.fwrite(record,db_name)
            return self.id
        
    def purge(self,db_name):
        self.file_obj=Storage(db_name)
        return self.file_obj.fpurge(db_name)

    def delete(self,db_name):
        if self.opendb(db_name):
            return self.file_obj.fdelete(db_name)
            


    
    
"""   
x=db()
x.view_records("table3")
print (x.find_numberof_records("table3"))
x.create("table3")
x.insert("table3",{"column":4,"column2":90})
print (x.find_numberof_records("table3"))
"""
