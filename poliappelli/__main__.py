from os import path
from sys import exit
from platform import system
from getpass import getpass
from warnings import catch_warnings

from poliappelli.parser import args
from poliappelli.scaper import Scraper


curr_dir = path.dirname(path.realpath(__file__))
login_file = 'poliappelli.txt' if system() == 'Windows' else '.poliappelli'


def credentials():
    current_path = f'{curr_dir}/{login_file}'
    home_path = f'{path.expanduser("~")}/{login_file}'

    if (path.exists(current_path) or path.exists(home_path)) and args.login:
        path_ = current_path if path.exists(current_path) else home_path
        with open(path_, 'r') as f:
            user, passwd = [entry.strip() for entry in f.readlines()]
    else:
        user = input('Username: ')
        passwd = getpass('Password: ')
        answer = input('Do you want to save your credentials? [Y/n]: ')

        if answer in ('', 'y', 'Y', 'yes', 'Yes', 'YES'):
            path_ = input('Path of credentials file [default=$HOME]: ')
            login = f'{path_}/{login_file}' if path_ != '' else home_path

            with open(login, 'w') as f:
                f.write(f'{user}\n{passwd}\n')
            print(f'Credentials stored in {login}\n')

    return user, passwd


def main():
    # per debug
    # if args.debug:
    #     Scraper().debug()
    #     exit()

    try:
        user, passwd = credentials()

        # core dello script
        with catch_warnings(record=True):
            Scraper(args, user, passwd)
    except KeyboardInterrupt:
        exit()


if __name__ == '__main__':
    main()
