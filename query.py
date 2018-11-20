from storage import Storage
from midlayer import Midlayer
import json
import re

class Query:
    def __init__(self):
        self.mid = Midlayer()
        self.retval=1

    def match(self,command):
        pattern = re.compile("(\w+)\.([a-z]+)\(([^\(\)]*)\)")
        matchobj = pattern.fullmatch(command)
        if matchobj is None:
            self.retval=101
            print ("Invalid query syntax")
            return self.retval
        self.tablename = matchobj.group(1)
        self.instr = matchobj.group(2)
        self.cond = matchobj.group(3)
        """
        self.tokens = command.split(".")
        if len(self.tokens)!=2:
            self.retval=101
            print ("Invalid query syntax")
            return self.retval
        
        self.tablename = self.tokens[0]
        self.instr, self.cond = self.tokens[1].split("(")
        self.cond = self.cond.strip(")")
        """
        #print (tablename, instr, cond)
        #self.parse()

        func = self.find_query()
        if isinstance(func, int):
            self.retval=101
            print ("Invalid query syntax")
            return self.retval
        
        func(self.tablename,self.cond)
        return self.retval

    def find_query(self):
        d = {
            "create" : self._create,
            "display" : self._display,
            #"showrow" : self.mid.displayrow,
            #"showcol" : self.mid.displaycol,
            "addrow" : self._addrow
            }
        try:
            func = d[self.instr]
        except KeyError:
            func = 101
        return func

    def _create(self,db_name,cond):
        self.mid.create(db_name)

    def _display(self,db_name,cond):
        data = self.mid.view_records(db_name)
        if data is not None:
            print (data)
        else:
            print ("DB does not exist")            

    def _addrow(self,db_name,cond):
        try:
            arg = json.loads(cond)
        except json.decoder.JSONDecodeError:
            print ("Wrong record format")
            return
        if self.mid.insert(db_name,arg) is not None:
            print ("Success")
        else:
            print ("DB does not exist")
        
        

while 1:
    q=input()
    obj=Query()
    obj.match(q)
        