import struct
import platform
import requests
import os
import subprocess

bits = str(struct.calcsize('P') * 8)
sys = platform.system()

versions = {
    "17.": {
        'Windows': {
            '64': 'https://download.oracle.com/java/17/latest/jdk-17_windows-x64_bin.exe',
            '32': 'https://download.oracle.com/java/17/latest/jdk-17_windows-x64_bin.exe',
        }
    },
    '1.8': {
        'Windows': {
            '64': 'https://javadl.oracle.com/webapps/download/AutoDL?BundleId=245479_4d5417147a92418ea8b615e228bb6935',
            '32': 'https://javadl.oracle.com/webapps/download/AutoDL?BundleId=245477_4d5417147a92418ea8b615e228bb6935',
        }
    },
    '1.7': {
        'Windows': {
            '64': 'https://rainbowsky.ru/download/jre-7u80-windows-x64.exe',
            '32': 'https://rainbowsky.ru/download/jre-7u80-windows-i586.exe',
        }
    },
}


def check_permission():
    try:
        os.chmod(os.getenv('SystemRoot'), 777)
    except PermissionError:
        print('Use administrator mode!')
        os.abort()


def env_set(version):

    print('Add JAVA_HOME to environment ...')
    java_s = os.path.join(os.environ['ProgramFiles'].replace(' (x86)', '').replace(' (x86)', ''), 'Java')
    os.chdir(java_s)

    for file in os.listdir():
        if version in file:
            java_home = os.path.join(java_s, file)
            break

    script_path = create_ps_script(java_home)
    args = ['powershell', '-executionpolicy', 'RemoteSigned', '-file', script_path]
    subprocess.call(args)
    os.remove(script_path)

    print('Added successful!')


def create_ps_script(path):
    string = f"[Environment]::SetEnvironmentVariable('JAVA_HOME', {repr(path)}, 'Machine')\n" \
             f"[Environment]::SetEnvironmentVariable('JAVA_HOME', {repr(path)}, 'User')\n"

    name = 'setter.ps1'
    print('Try create setting script...')
    with open(name, 'w') as file:
        file.write(string)
    print('Created!')
    return os.path.join(os.getcwd(), name)


def java_download(version):
    print(f'Downloading java of version {version}')
    root = os.getcwd()
    url = versions[version][sys][bits]
    s = requests.Session()
    get = s.get(url)
    tmp = os.environ['TMP']
    os.chdir(tmp)
    name = f'java_{version}.exe'

    with open(name, 'wb') as file:
        file.write(get.content)

    print('Java downloaded!')
    print('Try install ...')
    subprocess.call(name)
    os.chdir(root)
    os.remove(os.path.join(tmp, name))
    print('Installed!')
    env_set(version)