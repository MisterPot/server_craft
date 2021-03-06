import requests as rq
import os
import subprocess
import socket
import server_craft

versions = {
    '1.18.2': 'https://launcher.mojang.com/v1/objects/c8f83c5655308435b3dcf03c06d9fe8740a77469/server.jar',
    '1.18.1': 'https://launcher.mojang.com/v1/objects/125e5adf40c659fd3bce3e66e67a16bb49ecc1b9/server.jar',
    '1.17.1': 'https://launcher.mojang.com/v1/objects/a16d67e5807f57fc4e550299cf20226194497dc2/server.jar',
    '1.16.5': 'https://launcher.mojang.com/v1/objects/1b557e7b033b583cd9f66746b7a9ab1ec1673ced/server.jar',
    '1.15.2': 'https://launcher.mojang.com/v1/objects/bb2b6b1aefcd70dfd1892149ac3a215f6c636b07/server.jar',
    '1.14.4': 'https://launcher.mojang.com/v1/objects/3dc3d84a581f14691199cf6831b71ed1296a9fdf/server.jar',
    '1.13.2': 'https://launcher.mojang.com/v1/objects/3737db93722a9e39eeada7c27e7aca28b144ffa7/server.jar',
    '1.12.2': 'https://launcher.mojang.com/mc/game/1.12.2/server/886945bfb2b978778c3a0288fd7fab09d315b25f/server.jar',
}

to_java_versions = {
    '1.18.2': '17.',
    '1.18.1': '17.',
    '1.17.1': '17.',
    '1.16.5': '1.8',
    '1.15.2': '1.8',
    '1.14.4': '1.8',
    '1.13.2': '1.7',
    '1.12.2': '1.7',
}


def get_host_ip():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect(("8.8.8.8", 80))
    return sock.getsockname()[0]


class Download(object):

    def __init__(self, version: str):
        core = 'vanilla'
        if version.find(':') != -1:
            version, core = version.split(':')
        try:
            server_craft.get_ok(version)

        except server_craft.JavaNotFound:
            server_craft.check_permission()
            java_ver = to_java_versions[version]
            server_craft.java_download(java_ver)
            print('Restart your console with administrator mode!')
            os.abort()

        self.version = version
        self.core = core
        self.url = versions[version]
        self.jar_file = None

    def download(self, server_dir='.'):
        print('Try create server')
        try:
            os.chdir(server_dir)

        except FileNotFoundError:
            print('Wrong path to server directory!')

        path = server_craft.check_in_storage(self.version)

        if path:
            print('Server exist in chester, try copy')
            server_craft.copy_from_storage(self.version)
            print("Copied succsesful!")
        else:
            try:
                print('Downloading....')
                s = rq.Session()
                jar_request = s.get(self.url)
                print('Download successful!')
                path = server_craft.save_server_jar(self.version, jar_request)
                server_craft.copy_from_storage(self.version)

            except Exception:
                print('Download not successful.')
                print('Check your internet connection ! (may you use proxy ?)')
                return 0

        self.jar_file = path


        print('Unpacking....')

        self.__unpack()
        self.__change_properties()

    def __change_properties(self):
        print('Prepare file "server.properties"')
        host_ip = get_host_ip()
        free_port = server_craft.get_free_port()
        properties = server_craft.Properties('server.properties')
        properties.set('online-mode', 'false')
        properties.set('server-ip', host_ip)
        properties.set('difficulty', 'normal')
        properties.set('query.port', free_port)
        properties.set('server-port', free_port)
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
