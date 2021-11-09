import os
from argparse import ArgumentParser
import server_craft


def main():
    parser = ArgumentParser()
    parser.add_argument('-s', '--send', type=str, nargs=1, default=[], help='Send world to another user')
    parser.add_argument('-r', '--receive', type=str, nargs=1, default=[], help='Get world from player with current IP')

    args = parser.parse_args()

    recv = args.receive
    send = args.send

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
