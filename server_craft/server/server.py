from .config import Config
import pathlib
import os
import subprocess


class Server:

    def __init__(self):
        self.on = False
        self.serv_dir = os.getcwd()
        os.chdir(self.serv_dir)
        self.proc = None
        self.auto_save = True

    def set_serv_dir(self, serv_dir):
        self.serv_dir = pathlib.Path(serv_dir)
        os.chdir(self.serv_dir)

    def read_config(self, conf_file):
        conf = Config(conf_file)
        st = conf.start_props
        mem = conf.mem_props
        spec = conf.spec_props
        self.props = ['java']
        self.props.extend(mem)
        self.props.extend(['-jar', 'server.jar'])
        self.props.extend(st)

    def restart(self):
        self.stop()
        self.start()

    def start(self):
        self.on = True
        self.proc = subprocess.Popen(self.props,
                                     creationflags=(subprocess.CREATE_NEW_CONSOLE),
                                     stdin=subprocess.PIPE
                                     )

    def stop(self):
        self.on = False
        self.command('/stop')

    def command(self, command):
        self.proc.communicate(input=bytes(command, encoding='utf-8'))

    @property
    def status(self):
        return self.on
