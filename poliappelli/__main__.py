#!./venv/bin/python

from os import path
from sys import exit
from tqdm import tqdm
from platform import system
from getpass import getpass
from bs4 import BeautifulSoup
from urllib.request import urlopen
from warnings import catch_warnings
from datetime import datetime as dt
from argparse import ArgumentParser
from beautifultable import BeautifulTable, ALIGN_LEFT, STYLE_MARKDOWN

from selenium.webdriver import Firefox
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import WebDriverException

# inizializzazione degli argomenti
# che posso essere passati da shell
parser = ArgumentParser(
    description='Script delle date degli appelli del PoliTo.')
parser.add_argument(
    '-l', '--login', nargs='?', dest='login', default=True, const=False,
    type=bool, action='store', help="riscrivere le credenziali nel file .poliappelli")
parser.add_argument(
    '-s', '--sort', dest='order', nargs='?', default='Data',
    const='Data', type=str, help='ordinamento delle materie (default: Data)',
    choices=['Nome', 'Data', 'Tipo', 'Scadenza'])
parser.add_argument(
    '-o', '--output', nargs='?', dest='output', const='esami.md',
    type=str, help="scrive l'output su file (default: esami.md)")
parser.add_argument(
    '-d', '--debug', nargs='?', dest='debug', default=False, const=True,
    type=bool, help="flag per il parse di 'test.html'")
parser.add_argument(
    '-m', '--mesi', nargs='?', dest='mesi', default=4, const=12,
    type=int, help="range di mesi (default: 12 | non inserito: 4)"
)
args = parser.parse_args()

curr_dir = path.dirname(path.realpath(__file__))
login_file = 'poliappelli.txt' if system() == 'Windows' else '.poliappelli'

# costanti messaggio errore
RED = '\033[91m'
ENDC = '\033[0m'


class Scraper:
    def __init__(self, user=None, passwd=None):
        self.esami = list()
        self.user = user
        self.passwd = passwd
        print('Execution time depends on your connection, please be patient...')

    def _openfile(self, path):
        return urlopen('file:' + path).read()

    def _openurl(self, url):
        return urlopen(url).read()

    def debug(self):
        self.print_table(args.output, args.order, 'test.html')

    def find_table(self):
        # apre il browser Firefox per
        # accedere alla pagina del polito
        # e recuperare l'url termporaneo della
        # pagina degli appelli

        pbar = tqdm(total=100, desc='Scraping')

        # opzione per nascondere la finestra del browser
        opt = Options()
        opt.headless = True
        gecko = path.realpath('geckodriver') if path.exists('geckodriver') else 'geckodriver'

        try:
            driver = Firefox(options=opt, executable_path=gecko)
        except WebDriverException:
            print(RED + 'ERROR: geckodriver executable needs to be in PATH or in the current folder' + ENDC)
            exit(1)

        driver.get('https://idp.polito.it/idp/x509mixed-login')

        # TODO: caso di credenziali sbagliate

        # login al portale della didattica
        userElement = driver.find_element_by_id('j_username')
        passElement = driver.find_element_by_id('j_password')
        userElement.send_keys(self.user)
        passElement.send_keys(self.passwd)
        userElement.submit()

        pbar.update(25)

        # TODO: chiudere eventuali popup

        # TODO: caso di credenziali sbagliate
        WebDriverWait(driver, 20).until(EC.presence_of_element_located(
            (By.LINK_TEXT, 'Portale della Didattica')))
        driver.find_element_by_link_text('Portale della Didattica').click()

        pbar.update(25)

        # TODO: pagina non caricata
        WebDriverWait(driver, 20).until(EC.presence_of_element_located(
            (By.LINK_TEXT, 'Consultazione e prenotazione esami')))
        driver.find_element_by_link_text('Consultazione e prenotazione esami').click()

        pbar.update(25)

        # TODO: pagina non caricata
        WebDriverWait(driver, 20).until(EC.title_is('Prenotazione Esami'))
        if args.mesi != 4:
            form = driver.find_element_by_name('mesi_appelli')
            form.clear()
            form.send_keys(args.mesi)
            form.submit()
            WebDriverWait(driver, 20).until(EC.url_changes(driver.current_url))

        pbar.update(25)

        # TODO: pagina non caricata
        url = str(driver.current_url)

        driver.close()
        pbar.close()

        return url

    def parse_table(self, path_, tag='table'):
        # parsifica tutte le table che trova
        # nella pagina/file html e ne salva
        # i campi nella lista self.esami
        # ordinati per data dell'esame

        target = self._openfile(
            path_) if path_ is not None else self._openurl(self.find_table())

        prec = list()
        for table in BeautifulSoup(target, 'html.parser').find_all(tag):
            for tr in table.find_all('tr'):
                row = [cell.text.strip() for cell in tr.find_all('td')]
                if len(row) > 0:
                    # evita di lasciare campi vuoti
                    if row[1] == '':
                        row[1] = prec[1]

                    prec = row
                    self.esami.append(row)

    def print_table(self, out, order, path_=None):
        # crea una tabella (in sintassi markdown)
        # della lista esami che verra'
        # ordinata secondo il parametro order
        # stampata su terminale oppure su file

        self.parse_table(path_)
        self.sort(self.esami, order)
        print()

        table = BeautifulTable(
            max_width=200, default_alignment=ALIGN_LEFT)
        table.set_style(STYLE_MARKDOWN)
        table.column_headers = ['Nome', 'Data', 'Tipo', 'Scadenza', 'Aula']

        for materia in self.esami:
            table.append_row([
                materia[1],
                materia[2] if materia[2] is not '' else '?',
                materia[4],
                materia[6] if materia[6] is not '' else '?',
                ''])

        if out is None:
            print(table)
        else:
            with open(out, 'w') as f:
                f.write("## Esami\n\n")
                f.write(str(table))

    def sort(self, target, key):
        if key == 'Nome':
            target.sort(key=lambda materia: materia[1])
        elif key == 'Tipo':
            target.sort(key=lambda materia: materia[4])
        elif key == 'Scadenza':
            target.sort(key=lambda materia: dt.strptime(
                materia[6], "%d-%m-%Y %H:%M") if materia[6] is not ''
                else dt.strptime(materia[2], ""))
        else:
            target.sort(key=lambda materia: dt.strptime(
                materia[2], "%d-%m-%Y %H:%M") if materia[2] is not ''
                else dt.strptime(materia[2], ""))


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
    if args.debug:
        Scraper().debug()
        return

    try:
        user, passwd = credentials()

        # core dello script
        with catch_warnings(record=True):
            Scraper(user, passwd).print_table(args.output, args.order)
            print()
    except KeyboardInterrupt:
        exit()


if __name__ == '__main__':
    exit(main())
