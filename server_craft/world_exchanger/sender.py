import socket
import json


class Sender(object):
	def __init__(self, Adress=('localhost', 5000), MaxClient=1):
		self.s = socket.socket()
		self.s.bind(Adress)
		self.s.listen(MaxClient)

	def wait_for_con(self):

		self.Client, self.Adr=(self.s.accept())
		print('Connected!')

	def send_file(self, file_data):
		stringed = str(json.dumps(file_data))
		in_bytes = bytes(stringed, encoding='utf-8')
		print('Sending file data ...')
		self.Client.send(in_bytes)
		print("Done")
		with open(file_data['name'], 'rb') as file:
			raw_file = file.read()

		print("Sending file")
		self.Client.send(raw_file)
		print('Done')
