import os
from pathlib import Path
from server_craft import Properties
import shutil


class World(object):

    def __init__(self):
        properties = Properties('settings.conf', set_category=False)
        world_dir = properties.get('worldDir')
        self.world_name = properties.get('world')

        os.chdir(world_dir)

    def archive(self):
        filename = Path(shutil.make_archive(self.world_name, 'zip',
                                            root_dir='.',
                                            base_dir=self.world_name)).name
        new_filename = f'{filename.split(".")[0]}.world'
        os.rename(filename, new_filename)

        self.path = os.path.join(os.getcwd(), new_filename)
        return self.path

    def world_data(self):
        name = Path(self.path).name
        return {'name': name, 'size': os.path.getsize(name)}

    def del_archive(self):
        os.remove(self.path)
