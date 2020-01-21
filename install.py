import os
import sys
import glob
import shutil
import subprocess

MAIN = 'poliappelli/__main__.py'
URL = 'https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-linux64.tar.gz'
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


def install():
    if not os.path.exists('driver'):
        os.mkdir('driver')

    shell(f'curl -L {URL} | tar zxv -C driver')

    shell('poetry install --no-root')
    shell(f'poetry run pyinstaller {MAIN} -n poliappelli\
         --onefile --add-binary "./driver/geckodriver:./driver" --add-data "pyproject.toml:."')


def clean():
    for dir_ in TRASH:
        for file in glob.glob(f'{dir_}'):
            if os.path.isfile(file):
                os.remove(file)
            else:
                shutil.rmtree(file)


if __name__ == '__main__':
    install()
    clean()
