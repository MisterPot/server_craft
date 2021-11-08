from configparser import RawConfigParser as rp


class Properties(object):

	def __init__(self, properties_file, set_category=True):

		if set_category:

			with open(properties_file, 'r') as file:
				out = file.readlines()

			out.insert(2, '[server]')

			with open(properties_file, 'w') as file:
				file.writelines(out)

		self.parser = rp()
		self.parser.read(properties_file)
		self.file = properties_file

	def set(self, property_, value):
		self.parser.set('server', property_, value)

	def get(self, property_):
		return self.parser.get('server', property_)

	def confirm(self):
		self.parser.write(open(self.file, 'w'))

	def all_props(self):
		self.parser.values()