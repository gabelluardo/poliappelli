import re
import sys
import platform

from os import path
from tqdm import tqdm
from bs4 import BeautifulSoup
from urllib.request import urlopen
from datetime import datetime as dt
from beautifultable import BeautifulTable, ALIGN_LEFT, STYLE_MARKDOWN

from poliappelli.drivers import GECKODRIVERS

from selenium.webdriver import Firefox
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import WebDriverException, TimeoutException

# costanti messaggio errore
RED = '\033[91m'
ENDC = '\033[0m'


class Scraper:
    def __init__(self, args, user=None, passwd=None):
        self._user = user
        self._passwd = passwd
        self._root_url = 'https://idp.polito.it/idp/x509mixed-login'

        self._driver = self._init_browser()

        self.args = args
        self.esami = []
        self.table = None

    def _init_browser(self):
        opt = Options()
        opt.headless = True

        gecko = GECKODRIVERS[platform.system()]

        try:
            driver = Firefox(
                options=opt,
                executable_path=gecko,
                service_log_path='/dev/null'
            )
        except WebDriverException:
            print(f'{RED}ERROR: geckodriver executable needs to be in PATH or in the current folder{ENDC}')
            sys.exit(1)

        return driver

    def _write_file(self, path_):
        with open(path_, 'w') as f:
            f.write('## Esami\n\n'+str(self.table)+'\n')

    def _wait_and_click(self, text, timer=20):
        WebDriverWait(self._driver, timer).until(EC.presence_of_element_located(
            (By.LINK_TEXT, text)))
        self._driver.find_element_by_link_text(text).click()

    # def debug(self):
    #     self.print_table('test.html')

    def find_url(self):
        # apre il browser Firefox per
        # accedere alla pagina del polito
        # e recuperare l'url termporaneo della
        # pagina degli appelli

        driver = self._driver

        pbar = tqdm(total=100, desc='Scraping')

        driver.get(self._root_url)

        # TODO: caso di credenziali sbagliate

        # login al portale della didattica
        userElement = driver.find_element_by_id('j_username')
        passElement = driver.find_element_by_id('j_password')
        userElement.send_keys(self._user)
        passElement.send_keys(self._passwd)
        userElement.submit()

        pbar.update(25)

        try:
            self._wait_and_click('Portale della Didattica', 10)
        except TimeoutException:
            # prosegue se viene chiesto un cambio password
            driver.find_element_by_id('nocontinua').click()
            self._wait_and_click('Portale della Didattica', 10)
        # finally:

        pbar.update(25)

        # TODO: chiudere eventuali popup
        # TODO: pagina non caricata
        self._wait_and_click('Consultazione e prenotazione esami')

        pbar.update(25)

        # TODO: pagina non caricata
        WebDriverWait(driver, 20).until(EC.title_is('Prenotazione Esami'))
        if self.args.mesi != 4:
            form = driver.find_element_by_name('mesi_appelli')
            form.clear()
            form.send_keys(self.args.mesi)
            form.submit()
            WebDriverWait(driver, 20).until(EC.url_changes(driver.current_url))

        pbar.update(25)

        # TODO: pagina non caricata
        url = str(driver.current_url)

        driver.close()
        pbar.close()

        return url

    def parse_table(self, path, tag='table'):
        # parsifica tutte le table che trova
        # nella pagina/file html e ne salva
        # i campi nella lista self.esami
        # ordinati per data dell'esame

        target = urlopen(path).read()

        prec = []
        for table in BeautifulSoup(target, 'html.parser').find_all(tag):
            for tr in table.find_all('tr'):
                row = [cell.text.strip() for cell in tr.find_all('td')]
                if len(row) > 0:
                    # evita di lasciare campi vuoti
                    if row[1] == '':
                        row[1] = prec[1]

                    prec = row
                    self.esami.append(row)

    def run(self):
        # crea una tabella (in sintassi markdown)
        # della lista esami che verra'
        # ordinata secondo il parametro order
        # stampata su terminale oppure su file

        print('Execution time depends on your connection, please be patient...')

        out = self.args.file
        order = self.args.order

        url = self.find_url()

        self.parse_table(url)
        self.sort(self.esami, order)

        table = BeautifulTable(max_width=200, default_alignment=ALIGN_LEFT)
        table.set_style(STYLE_MARKDOWN)
        table.column_headers = ['Nome', 'Data', 'Tipo', 'Scadenza', 'Aula']

        for materia in self.esami:
            table.append_row([
                materia[1],
                materia[2] if materia[2] != '' else '?',
                materia[4],
                materia[6] if materia[6] != '' else '?',
                ''])

        self.table = table
        default = '{}/esami.md'

        if out is not None:
            # controllo che la destinazione sia una cartella
            # o un file con una estensione (es: .md, .txt, ecc)

            dest = default.format(re.sub(r'/+$', '', out)) if path.isdir(out) else out

            if path.isfile(dest):
                answer = input(f'\n\'{dest}\': already exists and will be rewritten.\
                    \nProceed anyway? [Y/n]: ')
                if answer not in ('', 'y', 'Y', 'yes', 'Yes', 'YES'):
                    exit()

            if len(re.findall(r'\..+$', dest)) > 0:
                self._write_file(dest)
                print(f'\nTable written in: {dest}')
            else:
                print(f'\n{RED}\'{dest}\': is not a valid file or directory{ENDC}')
        else:
            print('\n'+str(table)+'\n')

    def sort(self, target, key):
        if key == 'Nome':
            target.sort(key=lambda materia: materia[1])
        elif key == 'Tipo':
            target.sort(key=lambda materia: materia[4])
        elif key == 'Scadenza':
            target.sort(key=lambda materia: dt.strptime(
                materia[6], '%d-%m-%Y %H:%M') if materia[6] != ''
                else dt.strptime(materia[2], ''))
        else:
            target.sort(key=lambda materia: dt.strptime(
                materia[2], '%d-%m-%Y %H:%M') if materia[2] != ''
                else dt.strptime(materia[2], ''))
