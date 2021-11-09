import socket
import json


class Client(object):
	def __init__(self, Adress=('localhost', 5000)):
		self.s = socket.socket()
		self.s.connect(Adress)

	def get_file(self):
		b = self.s.recv(1024)
		print('File data received!')
		file_data = json.loads(b.decode())

		print('Try receive file')
		raw_file = self.s.recv(file_data['size'])
		print('Done.')
		print(f'Write file with name - {file_data["name"]}')
		with open(file_data['name'], 'wb') as file:
			file.write(raw_file)
		print('Writed')

	def close(self):
		self.s.close()
