from argparse import ArgumentParser
import subprocess
import server_craft
from server_craft import versions, Download
import os

def main():
	parser = ArgumentParser()
	parser.add_argument('-d', '--download',type=str, nargs='*', help='Download this version of minecraft', default=False)
	parser.add_argument('-r', '--run', default=False, type=bool, nargs='?',const='default',help='Run the server in current dir')
	parser.add_argument('-v', '--versions', default=False, nargs='?', const='default',type=bool, help='Print list of available versions')
	parser.add_argument('-c', '--config', default=server_craft.default_config, type=str, help='Config file for start server')
	args = parser.parse_args()

	if args.versions:
		print(list(versions.keys()))
		os._exit(0)

	if args.config == 'create':
		with open(server_craft.default_config, 'rb') as file:
			out = file.read()

		with open(os.path.join(os.getcwd(), 'settings.conf'), 'wb') as file:
			file.write(out)

		os._exit(0)

	if args.download:
		d = Download(args.download[0])
		try:
			d.download(args.download[1])
		except IndexError:
			d.download()

	if args.run:
		os.environ['config'] = args.config
		subprocess.run('py')