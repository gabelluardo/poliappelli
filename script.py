#!./venv/bin/python3

import sys
from bs4 import BeautifulSoup
from beautifultable import BeautifulTable
from datetime import datetime as dt
import urllib.request
import os.path


class TABparser:
    def __init__(self):
        self.esami = list()

    def _openfile(self, path):
        return urllib.request.urlopen('file:' + path).read()

    def _openurl(self, url):
        return urllib.request.urlopen(url).read()

    def _sort(self, key='Data'):
        # TODO: aggiungere flag per l'ordinamento
        if key is 'Data':
            self.esami.sort(key=lambda materia: dt.strptime(
                materia[2], "%d-%m-%Y %H:%M"))

    def parse(self, path, tag='table'):
        ## parsifica tutte le table che trova
        ## nella pagina/file html e ne salva
        ## i campi nella lista self.esami
        ## ordinati per data dell'esame

        target = self._openfile(path) if os.path.isfile(
            path) else self._openurl(path)

        for table in BeautifulSoup(target, "lxml").find_all(tag):
            for tr in table.find_all('tr'):
                row = [cell.text.strip() for cell in tr.find_all('td')]
                if row.__len__() > 0:
                    self.esami.append(row)

        self._sort()

    def output(self, filename='esami.md', terminal=False):
        ## crea una tabella in sintassi markdonw
        ## della lista self.esami che verra'
        ## stampata su terminale oppure su file

        table = BeautifulTable(
            max_width=200, default_alignment=BeautifulTable.ALIGN_LEFT)
        table.set_style(BeautifulTable.STYLE_MARKDOWN)
        table.column_headers = ['Nome', 'Data', 'Tipo', 'Scadenza', 'Aula']

        for materia in self.esami:
            table.append_row([
                materia[1], materia[2], materia[4], materia[6], ''])

        if terminal:
            print(table)
        else:
            file = open(filename, 'w')
            file.write("## Esami\n\n")
            file.write(str(table))
            file.close()


def main():
    # TODO: flag linea di comando

    hp = TABparser()
    hp.parse('test.html')
    hp.output(terminal=False)


if __name__ == '__main__':
    sys.exit(main())
