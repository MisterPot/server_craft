from .server.server import Server
import os

def start():
	server = Server()
	config_file = os.environ.get('config')
	server.read_config(config_file)
	return server

server = start()