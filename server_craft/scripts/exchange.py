import os
from argparse import ArgumentParser
import server_craft
import shutil


def main():
    parser = ArgumentParser()
    parser.add_argument('-l', '--list', nargs='?', const='default', default=False, type=bool,
                        help="Print all saved worlds in storage")
    parser.add_argument('-s', '--send', type=str, nargs=1, default=[], help='Send world to another user')
    parser.add_argument('-r', '--receive', type=str, nargs=1, default=[], help='Get world from player with current IP')
    parser.add_argument('-i', '--insert', type=str, nargs=1, help='Insert saved world in current dir')

    args = parser.parse_args()

    l = args.list
    recv = args.receive
    send = args.send
    ins = args.insert

    if l:
        os.chdir(server_craft.worlds_storage_path)
        print([ file.split('.')[0] for file in os.listdir() if file not in ['__init__.py', '__pycache__']])
        os._exit(0)

    if ins:
        file = f"{ins[0]}.world"
        path = os.path.join(server_craft.worlds_storage_path, file)
        shutil.unpack_archive(path, '.', 'zip')

    if recv:
        try:
            address, port = recv[0].split(':')

        except ValueError:
            address = recv[0]
            port = 5000

        os.chdir(server_craft.worlds_storage_path)
        client = server_craft.Client(Adress=(address, port))
        client.get_file()
        client.close()

    if send:
        try:
            host_ip = server_craft.get_host_ip()
            sender = server_craft.Sender(Adress=(host_ip, 5000))
            world = server_craft.World()
            world.archive()
            world_data = world.world_data()
            sender.wait_for_con()
            sender.send_file(world_data)
            world.del_archive()

        except Exception:
            raise Exception('Any error occurred')
