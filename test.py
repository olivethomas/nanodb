import os
import json
import os.path


class JSONStorage():
	def __init__(self, path):
		self.create_file(path)
		self.path = path
		self.handle = open(path, 'r+')

	def close(self):
		self.handle.close()

	def read(self, is_ordered_dict = False):
		self.handle.seek(0)
		return json.load(self.handle)

	def write(self, data):
		# print data
		self.handle.seek(0)
		json.dump(data, self.handle)
		self.handle.flush()
		self.handle.truncate()

	def create_file(self, file, times=None):
		if not os.path.exists(file):
			with open(file, 'a') as f:
				os.utime(file, times)
				json.dump({}, f)


file = JSONStorage("abcd.json")
file.write({"h2":"hii"})
file.write({"h3":"hii"})
file.close()
