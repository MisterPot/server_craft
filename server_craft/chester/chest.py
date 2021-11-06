import server_craft
import os
import json
import re
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
    print("Refresh chester storage")
    ls = os.listdir()

    data = {}
    for filename in ls:

        if filename in ['__init__.py', '__pycache__']:
            continue

        version = re.search(r'\d\S+\d', filename)
        data[version.group().replace('_', '.')] = os.path.join(os.getcwd(), filename)

    os.chdir('..')
    with DFile('downloaded.json') as file:
        file.bufer = json.dumps(data)
        file.write('')
    print("Refreshed")

def copy_from_storage(version):
    refresh_storage()
    root = os.getcwd()
    @return_to(server_craft.storage_path)
    def copy(dst_path):
        with open(dst_path, 'rb') as file:
            out = file.read()

        with open(os.path.join(root, pathlib.Path(dst_path).name), 'wb') as file:
            file.write(out)

    dst_path = check_in_storage(version)

    if dst_path:
        copy(dst_path)
    else:
        raise FileNotFoundError("Server of current version isn't downloaded !")


@return_to(server_craft.storage_path, parent=1)
def save_to_json(filename):
    print('Try save to path to server jar-file')
    version = re.search(r'\d\S+\d', filename).group().replace("_", '.')
    with DFile('downloaded.json') as file:
        out = json.loads(file.read())
        out[version] = os.path.join(server_craft.storage_path, filename)
        file.bufer = json.dumps(out)
        file.write('')
    print('OK')

@return_to(server_craft.storage_path)
def save_server_jar(version, request):
    print('Try save server jar')
    file_name = f'jar_{version.replace(".", "_")}.jar'
    save_to_json(file_name)
    with open(file_name, 'wb') as file:
        file.write(request.content)
    print('Saved')

    return os.path.join(os.getcwd(), file_name)
