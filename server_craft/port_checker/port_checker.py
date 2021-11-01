from telnetlib import Telnet
from server_craft.download.download import get_host_ip


def get_free_port():

    start_port = 25565
    host = get_host_ip()

    while True:
        print(f'Try use port - {start_port}')
        try:
            with Telnet(host, start_port):
                print(f'Port already used - {start_port}')

        except ConnectionRefusedError:
            print(f'Use free port - {start_port}')
            return str(start_port)

        start_port -= 1
