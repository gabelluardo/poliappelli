#!/usr/bin/python3

from bs4 import BeautifulSoup
import urllib.request
import sys


def main():
    #url = "https://sid.studenti.polito.it/prenoesami/signin.do?event=verifySignin&id=173760105&tok=53616C7465645F5FACA0C62FFB1B2D8BD5DB7CFE87AA4342E8A5ABEDDDD0B80121CBA658743EA322D9E1C60480383D65A4F6C352D03635A01F74A4558B2A4BFDA20603E51BAB067EE339B990175D4952"
    #page = urllib.request.urlopen(url).read()

    filein = urllib.request.urlopen('file:test.html').read()

    soup = BeautifulSoup(filein, "lxml")

    esami = list()

    tables = soup.find_all('table')

    for table in tables:
        table_rows = table.find_all('tr')

        for tr in table_rows:
            td = tr.find_all('td')
            row = [i.text.strip() for i in td]
            if row != []:
                esami.append(row)

    file = open('esami.md', 'w')
    file.write("## Esami\n" +
               "| Nome | Data | Tipo | Scadenza | Aula |\n" +
               "|------|------|------|----------|------|\n"
               )

    for materia in esami:
        file.write('|{}|{}|{}|{}|{}|\n'.format(
            materia[1], materia[2], materia[4], materia[6], ''))


if __name__ == '__main__':
    sys.exit(main())
