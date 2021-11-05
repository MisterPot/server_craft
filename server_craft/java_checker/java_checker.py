import subprocess


class JavaNotFound(Exception):

    def __str__(self):
        return 'Java not found'


class VersionNotSupported(Exception):

    def __str__(self):
        return 'This server version not supported'


def get_version():
    proc = subprocess.run(['java', '--version'], stdout=subprocess.PIPE)

    try:
        vers = proc.stdout.decode().split(' ')[1]
    except Exception:
        proc = subprocess.run(['java', '-version'], stderr=subprocess.PIPE)
        vers = proc.stderr.decode().split(' ')[1]

    try:
        float(vers[:3])
    except ValueError:
        raise JavaNotFound()

    return vers[:3]


versions = {
    '17': ['1.17.1'],
    '1.8': ['1.16.5', '1.15.2', '1.14.4', '1.13.2', '1.12.2'],
    '1.7': ['1.15.2', '1.14.4', '1.13.2', '1.12.2'],
}


def get_ok(server_v):
    version = get_version()

    if server_v in versions[version]:
        return True

    for version_ in versions.keys():
        if version > version_:
            if server_v in versions[version_]:
                return True

    else:
        raise VersionNotSupported()
