from .server.server import Server
from .server.config import Config
from .server.properties import Properties
from .download.download import Download, versions
import pathlib
import os

root = __path__[0]

default_config = os.path.join(root, pathlib.Path('server\\settings.conf'))
