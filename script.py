#!/usr/bin/python3

from bs4 import BeautifulSoup
import urllib.request
import sys
import os.path


class TABparser:
    def __init__(self):
        self.esami = list()

    def _openfile(self, path):
        return urllib.request.urlopen('file:' + path).read()

    def _openurl(self, url):
        return urllib.request.urlopen(url).read()

    def parse(self, path, tag='table'):
        target = self._openfile(path) if os.path.isfile(path) else self._openurl(path)

        for table in BeautifulSoup(target, "lxml").find_all(tag):
            for tr in table.find_all('tr'):
                row = [cell.text.strip() for cell in tr.find_all('td')]
                if row.__len__() > 0:
                    self.esami.append(row)

    def output(self, filename='esami.md'):
        file = open(filename, 'w')
        file.write("## Esami\n\n"
                   + "| Nome | Data | Tipo | Scadenza | Aula |\n"
                   + "|------|------|------|----------|------|\n")

        for materia in self.esami:
            file.write('|{}|{}|{}|{}|{}|\n'.format(
                materia[1], materia[2], materia[4], materia[6], ''))


def main():

    # url a scadenza
    url='https://sid.studenti.polito.it/prenoesami/signin.do?event=verifySignin&id=173772749&tok=53616C7465645F5FA7FD14F2EA5FB01899AFCEDFFA45DAF7D4287F72BFE1B16FDB944AFCF5690216AA606CB9EB0561725B9E69D91C90E606C822AC29BD7051BD40717F1B5E4AA36963F178CEA502A92A'

    hp = TABparser()
    #hp.parse('test.html')
    hp.parse(url)
    hp.output()


if __name__ == '__main__':
    sys.exit(main())
