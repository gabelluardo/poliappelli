import os
import sys
import glob
import shutil
import platform
import subprocess

from poliappelli import __version__


MAIN = 'poliappelli/__main__.py'
BINARY_NAME = f'poliappelli-{__version__}-{platform.system().lower()}{platform.architecture()[0][:2]}'

DRIVER_VERSION = 'v0.26.0'
URL = {
    'Windows': f'https://github.com/mozilla/geckodriver/releases/download/{DRIVER_VERSION}/geckodriver-{DRIVER_VERSION}-win64.zip',
    'Darwin': f'https://github.com/mozilla/geckodriver/releases/download/{DRIVER_VERSION}/geckodriver-{DRIVER_VERSION}-macos.tar.gz',
    'Linux': f'https://github.com/mozilla/geckodriver/releases/download/{DRIVER_VERSION}/geckodriver-{DRIVER_VERSION}-linux64.tar.gz',
}
TRASH = [
    '*/__pycache__/',
    'build/',
    '*.spec',
    '*.log',
    '*.egg-info',
    'driver/',
    '.venv'
]


def shell(cmd):
    try:
        with subprocess.Popen(cmd, shell=True):
            pass
    except KeyboardInterrupt:
        pass


def driver(systems=None):
    if not os.path.exists('driver'):
        os.mkdir('driver')

    urls = URL.values() if systems else [URL[platform.system()]]

    for url in urls:
        if url[-3:] == 'zip':
            filename = url.split('/')[-1][:-4]
            unzip = f'gzip -dc > driver/{filename}'
        else:
            filename = url.split('/')[-1][:-7]
            unzip = f'tar zxv --transform "s|.*|{filename}|" -C driver'

        shell(f'curl -LZ {url} | {unzip} && chmod +x driver/*')


def install(systems):
    driver(systems)
    shell('poetry install --no-root')
    shell(f'poetry run pyinstaller {MAIN} --onefile --noconsole -n {BINARY_NAME}\
         --add-binary "driver/geckodriver*:driver"\
         --add-data "pyproject.toml:."')


def clean():
    for dir_ in TRASH:
        for file in glob.glob(f'{dir_}'):
            if os.path.isfile(file):
                os.remove(file)
            else:
                shutil.rmtree(file)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.argv.append(None)

    if sys.argv[1] == 'driver':
        driver()
    else:
        install(True if sys.argv[1] == 'all' else None)
        clean()
