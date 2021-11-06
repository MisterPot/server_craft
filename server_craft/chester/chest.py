import server_craft
import os
import json
import re
import shutil
import pathlib


class DFile(object):

    def __init__(self, filename):
        self.filename = filename
        self.bufer = ''

        if os.path.exists(filename):
            pass

        else:
            with open(filename, 'w') as file:
                pass

    def __bufer(self):
        with open(self.filename, 'r') as file:
            self.bufer += file.read()

    def replace(self, pattern, string):
        self.bufer = self.bufer.replace(pattern, string)
        self.write('')

    def write(self, text):
        self.bufer += text
        with open(self.filename, 'w') as file:
            file.write(self.bufer)

    def cl_buf(self):
        self.bufer = ''

    def cl_file(self):
        with open(self.filename, 'w'):
            pass

    def read(self):
        self.cl_buf()
        self.__bufer()
        return self.bufer

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


def return_to(path, parent=None):
    def f(func):
        def arg(*args, **kwargs):
            root = os.getcwd()
            to_path = pathlib.Path(path)

            if parent:
                for i in range(0, parent):
                    to_path = to_path.parent
            os.chdir(to_path)
            res = func(*args, **kwargs)
            os.chdir(root)
            return res
        return arg
    return f


@return_to(server_craft.storage_path, parent=1)
def check_in_storage(version):
    with DFile('downloaded.json') as file:
        out = json.loads(file.read())

    path = out.get(version)
    return path


@return_to(server_craft.storage_path)
def refresh_storage():
    ls = os.listdir()

    data = {}
    for filename in ls:
        version = re.search(r'\d\S+\d', filename)
        data[version.group().replace('_', '.')] = os.path.join(os.getcwd(), filename)

    os.chdir('..')
    with DFile('downloaded.json') as file:
        file.write(json.dumps(data))


def copy_from_storage(version):
    refresh_storage()

    @return_to(server_craft.storage_path)
    def copy(dst_path):
        shutil.copyfile(os.getcwd(), dst_path)

    dst_path = check_in_storage(version)

    if dst_path:
        copy(dst_path)
    else:
        raise FileNotFoundError("Server of current version isn't downloaded !")


@return_to(server_craft.storage_path, parent=1)
def save_to_json(filename):
    version = re.search(r'\d\S+\d', filename).group().replace("_", '.')
    with DFile('downloaded.json') as file:
        out = json.loads(file.read())
        out[version] = os.path.join(server_craft.storage_path, filename)
        file.write(json.dumps(out))


@return_to(server_craft.storage_path)
def save_server_jar(version, request):
    file_name = f'jar_{version.replace(".", "_")}.jar'
    save_to_json(file_name)
    with open(file_name, 'wb') as file:
        file.write(request.content)

    return os.path.join(os.getcwd(), file_name)
