import requests as rq
import os
import subprocess
import socket
from server_craft import Properties


versions = {
	'1.17.1': 'https://launcher.mojang.com/v1/objects/a16d67e5807f57fc4e550299cf20226194497dc2/server.jar',
	'1.16.5': 'https://launcher.mojang.com/v1/objects/1b557e7b033b583cd9f66746b7a9ab1ec1673ced/server.jar',
	'1.15.2': 'https://launcher.mojang.com/v1/objects/bb2b6b1aefcd70dfd1892149ac3a215f6c636b07/server.jar',
	'1.14.4': 'https://launcher.mojang.com/v1/objects/3dc3d84a581f14691199cf6831b71ed1296a9fdf/server.jar',
	'1.13.2': 'https://launcher.mojang.com/v1/objects/3737db93722a9e39eeada7c27e7aca28b144ffa7/server.jar',
	'1.12.2': 'https://launcher.mojang.com/mc/game/1.12.2/server/886945bfb2b978778c3a0288fd7fab09d315b25f/server.jar',
}

def get_host_ip():
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.connect(("8.8.8.8", 80))
	return sock.getsockname()[0]


class Download(object):

	def __init__(self, version):

		self.version = version
		self.url = versions[version]
		self.jar_file = None

	def download(self, server_dir='.'):
		print('Downloading....')
		try:
			os.chdir(server_dir)

		except FileNotFoundError:
			print('Wrong path to server directory!')

		try:
			s = rq.Session()
			jar = s.get(self.url).content

		except Exception:
			print('Download not successful.')
			print('Check your internet connection ! (may you use proxy ?)')

		with open('server.jar', 'wb') as file:
			file.write(jar)

		self.jar_file = os.path.join(os.getcwd(), 'server.jar')

		print('Download successful!')
		print('Unpacking....')

		self.__unpack()
		self.__change_properties()

	def __change_properties(self):

		print('Prepare file "server.properties"')
		with open('server.properties', 'r') as file:
			out = file.readlines()

		out.insert(2, '[server]')

		with open('server.properties', 'w') as file:
			file.writelines(out)

		host_ip = get_host_ip()
		properties = Properties('server.properties')
		properties.set('online-mode', 'false')
		properties.set('server-ip', host_ip)
		properties.set('difficulty', 'normal')
		properties.confirm()
		print('Seted online-mode = false')
		print(f'Seted server-ip = {host_ip}')
		print('Now use Server object to run this server')

	def __unpack(self):

		proc = subprocess.run(['java', '-jar', self.jar_file],
		 					  stderr=subprocess.DEVNULL,
		 					  stdout=subprocess.DEVNULL)

		with open('eula.txt', 'r') as file:
			out = file.readlines()

		confirm = out[len(out) - 1].replace('false', 'true')
		out[len(out) - 1] = confirm

		with open('eula.txt', 'w') as file:
			file.writelines(out)

		print('Unpacked successful!')
		print('Eula is true')