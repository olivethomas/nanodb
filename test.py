import json
fptr=open("table4.json","r")
data = json.loads(fptr.read())
print(data["1"]["name"])
print(data["1"]["name"][0])
