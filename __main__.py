#!./venv/bin/python3

import sys
import argparse
import urllib.request
import getpass

from tqdm import tqdm
from bs4 import BeautifulSoup
from beautifultable import BeautifulTable
from datetime import datetime as dt
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options


# inizializzazione degli argomenti
# che posso essere passati da shell
parser = argparse.ArgumentParser(
    description='Script delle date degli appelli del PoliTo.')
parser.add_argument(
    '-u', '--user', dest='username', type=str, action='store',
    help="inserimento esplicito dell'username")
parser.add_argument(
    '-p', '--passwd', dest='passwd', type=str, action='store',
    help="inserimento esplicito della password (sconsigliato)")
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


class Scraper:
    def __init__(self, user=None, passwd=None):
        self.esami = list()
        self.user = user
        self.passwd = passwd

    def _openfile(self, path):
        return urllib.request.urlopen('file:' + path).read()

    def _openurl(self, url):
        return urllib.request.urlopen(url).read()

    def debug(self):
        self.print_table(args.output, args.order, 'test.html')

    def find_table(self):
        # apre il browser Firefox per
        # accedere alla pagina del polito
        # e recuperare l'url termporaneo della
        # pagina degli appelli

        url = str()
        pbar = tqdm(total=100, desc='Scraping')

        # opzione per nascondere la finestra del browser
        opt = Options()
        opt.headless = True

        driver = webdriver.Firefox(
            options=opt, executable_path="./geckodriver")
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
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.LINK_TEXT, 'Portale della Didattica')))
        driver.find_element_by_link_text('Portale della Didattica').click()

        pbar.update(25)

        # TODO: pagina non caricata
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.LINK_TEXT, 'Consultazione e prenotazione esami')))
        driver.find_element_by_link_text(
            'Consultazione e prenotazione esami').click()

        pbar.update(25)

        # TODO: pagina non caricata
        WebDriverWait(driver, 10).until(EC.title_is('Prenotazione Esami'))
        if args.mesi != 4:
            form = driver.find_element_by_name('mesi_appelli')
            form.clear()
            form.send_keys(args.mesi)
            form.submit()
            WebDriverWait(driver, 10).until(EC.url_changes(driver.current_url))

        pbar.update(25)

        # TODO: pagina non caricata
        url = driver.current_url

        driver.close()
        pbar.close()

        return url

    def parse_table(self, path, tag='table'):
        # parsifica tutte le table che trova
        # nella pagina/file html e ne salva
        # i campi nella lista self.esami
        # ordinati per data dell'esame

        target = self._openfile(
            path) if path is not None else self._openurl(self.find_table())

        prec = list()
        for table in BeautifulSoup(target, "lxml").find_all(tag):
            for tr in table.find_all('tr'):
                row = [cell.text.strip() for cell in tr.find_all('td')]
                if row.__len__() > 0:
                    # evita di lasciare campi vuoti
                    if row[1] == '':
                        row[1] = prec[1]
                    prec = row

                    self.esami.append(row)

    def print_table(self, out, order, path=None):
        # crea una tabella (in sintassi markdown)
        # della lista esami che verra'
        # ordinata secondo il parametro order
        # stampata su terminale oppure su file

        self.parse_table(path)
        self.sort(self.esami, order)

        table = BeautifulTable(
            max_width=200, default_alignment=BeautifulTable.ALIGN_LEFT)
        table.set_style(BeautifulTable.STYLE_MARKDOWN)
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


def main():
    # per debug
    if args.debug:
        Scraper().debug()
        return

    # core dello script
    user = input('Username: ') if args.username is None else args.username
    passwd = getpass.getpass('Password: ') if args.passwd is None else args.passwd
    Scraper(user, passwd).print_table(args.output, args.order)


if __name__ == '__main__':
    sys.exit(main())
