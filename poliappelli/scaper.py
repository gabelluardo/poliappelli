import re

from os import path
from tqdm import tqdm
from bs4 import BeautifulSoup
from urllib.request import urlopen
from datetime import datetime as dt
from beautifultable import BeautifulTable, ALIGN_LEFT, STYLE_MARKDOWN

from selenium.webdriver import Firefox
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import WebDriverException

# costanti messaggio errore
RED = '\033[91m'
ENDC = '\033[0m'


class Scraper:
    def __init__(self, args, user=None, passwd=None):
        self.user = user
        self.passwd = passwd
        self.args = args

        self.esami = list()
        self.table = None

        print('Execution time depends on your connection, please be patient...')
        self.print_table()

    def _openfile(self, path):
        return urlopen('file:' + path).read()

    def _openurl(self, url):
        return urlopen(url).read()

    def _write_file(self, path_):
        with open(path_, 'w') as f:
            f.write('## Esami\n\n'+str(self.table)+'\n')

    # def debug(self):
    #     self.print_table('test.html')

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
            driver = Firefox(
                options=opt,
                executable_path=gecko,
                service_log_path='/dev/null'
            )
        except WebDriverException:
            print('{RED}ERROR: geckodriver executable needs to be in PATH or in the current folder{ENDC}')
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

    def print_table(self, path_=None):
        # crea una tabella (in sintassi markdown)
        # della lista esami che verra'
        # ordinata secondo il parametro order
        # stampata su terminale oppure su file
        out = self.args.file
        order = self.args.order

        self.parse_table(path_)
        self.sort(self.esami, order)

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
                materia[6], '%d-%m-%Y %H:%M') if materia[6] is not ''
                else dt.strptime(materia[2], ''))
        else:
            target.sort(key=lambda materia: dt.strptime(
                materia[2], '%d-%m-%Y %H:%M') if materia[2] is not ''
                else dt.strptime(materia[2], ''))
