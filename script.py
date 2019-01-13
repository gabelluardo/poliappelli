#!./venv/bin/python3

import sys
import argparse
import urllib.request
import os.path
from bs4 import BeautifulSoup
from beautifultable import BeautifulTable
from datetime import datetime as dt


class Scraper:
    def __init__(self):
        self.esami = list()

    def _openfile(self, path):
        return urllib.request.urlopen('file:' + path).read()

    def _openurl(self, url):
        return urllib.request.urlopen(url).read()

    def tab_parse(self, path, tag='table'):
        # parsifica tutte le table che trova
        # nella pagina/file html e ne salva
        # i campi nella lista self.esami
        # ordinati per data dell'esame

        target = self._openfile(path) if os.path.isfile(
            path) else self._openurl(path)

        for table in BeautifulSoup(target, "lxml").find_all(tag):
            for tr in table.find_all('tr'):
                row = [cell.text.strip() for cell in tr.find_all('td')]
                if row.__len__() > 0:
                    self.esami.append(row)
        return self.esami


def main():
    # inizializzazione degli argomenti
    # che posso essere passati da shell

    parser = argparse.ArgumentParser(
        description='Script le date degli appelli del PoliTo.')
    parser.add_argument('-s', '--sort', dest='sorted', nargs='?', default='Data', const='Data', type=str,
                        help='ordinamento delle materie (default: Data)', choices=['Nome', 'Data', 'Tipo', 'Scadenza'])
    parser.add_argument('-o', '--output', nargs='?', dest='output', const='esami.md',
                        type=str, help="scrive l'output su file (default: esami.md)")
    args = parser.parse_args()

    # core dello script
    esami = Scraper().tab_parse('test.html')
    print_table(esami, args.output, args.sorted)


def print_table(esami, filename, sort_flag):
    # crea una tabella (in sintassi markdown)
    # della lista esami che verra'
    # ordinata secondo il sort_flag
    # stampata su terminale oppure su file
    sort(esami, sort_flag)

    table = BeautifulTable(
        max_width=200, default_alignment=BeautifulTable.ALIGN_LEFT)
    table.set_style(BeautifulTable.STYLE_MARKDOWN)
    table.column_headers = ['Nome', 'Data', 'Tipo', 'Scadenza', 'Aula']

    for materia in esami:
        table.append_row([
            materia[1], materia[2], materia[4], materia[6], ''])

    if filename is None:
        print(table)
    else:
        file = open(filename, 'w')
        file.write("## Esami\n\n")
        file.write(str(table))
        file.close()


def sort(target, key='Data'):
    if key == 'Nome':
        target.sort(key=lambda materia: materia[1])
    elif key == 'Tipo':
        target.sort(key=lambda materia: materia[4])
    elif key == 'Scadenza':
        target.sort(key=lambda materia: dt.strptime(
            materia[6], "%d-%m-%Y %H:%M"))
    else:
        target.sort(key=lambda materia: dt.strptime(
            materia[2], "%d-%m-%Y %H:%M"))


if __name__ == '__main__':
    sys.exit(main())
