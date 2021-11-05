import server_craft
import os
import json
import shutil
import pathlib


def return_to(path, parent=None):
    def f(func):
        def arg(*args, **kwargs):
            root = os.getcwd()
            to_path = pathlib.Path(path)

            if parent:
                for i in range(0, parent):
                    to_path = to_path.parent
            os.chdir(to_path)
            func(*args, **kwargs)
            os.chdir(root)
        return arg
    return f


@return_to(server_craft.storage_path, parent=1)
def save_to_json(version, path):

    with open('downloaded.json', 'r') as file:
        out = json.load(file)

    out[version] = path

    with open('downloaded.json', 'w') as file:
        file.write(json.dumps(out))


@return_to(server_craft.storage_path)
def save_server_jar(version, request=None, filename=None):
    file_name = f'jar_{version}.jar'

    with open(file_name, 'wb') as file:
        if request:
            file.write(request.content)

        elif filename:
            with open(filename, 'rb') as file2:
                out = file2.read()
            file.write(out)

        else:
            file.write(b'')