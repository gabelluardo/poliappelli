# Poliappelli

Script per ricordare tutte le date degli appelli del PoliTo

### Build

**Richiesti:**

-   python3
-   pipenv
-   make

lanciare la compilazione con `make`

### Uso

    ./script 

Le credenziali saranno salvate in `.login.txt`, per aggiornale usare:

    ./script -l

per tutte le altre opzioni: `./script -h`
```
usage: script [-h] [-l [LOGIN]] [-s [{Nome,Data,Tipo,Scadenza}]] [-o [OUTPUT]] [-d [DEBUG]] [-m [MESI]]

optional arguments:
  -h, --help                            show this help message and exit
  -l [LOGIN], --login [LOGIN]           riscrivere le credenziali nel file .login.txt
  -s [{Nome,Data,Tipo,Scadenza}], 
    --sort [{Nome,Data,Tipo,Scadenza}]  ordinamento delle materie (default: Data)
  -o [OUTPUT], --output [OUTPUT]        scrive l'output su file (default: esami.md)
  -d [DEBUG], --debug [DEBUG]           flag per il parse di 'test.html'
  -m [MESI], --mesi [MESI]              range di mesi (default: 12 | non inserito: 4)
```

### Prestazioni

14 secondi

### SO

Linux  
Windows (forse, ma con un altro [geckodriver](https://github.com/mozilla/geckodriver/releases))

### License

GNU GPL3  
[Geckodriver](https://github.com/mozilla/geckodriver) è software Mozilla sotto MPL


--- 

### Doc

-   [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
-   [Selenium](https://selenium-python.readthedocs.io/)
-   [BeautifulTable](https://beautifultable.readthedocs.io/en/latest/index.html)
-   [Argparser](https://docs.python.org/3.6/library/argparse.html#module-argparse)
-   [PyInstaller](https://pyinstaller.readthedocs.io/en/stable/)


### TODO

-   [x] beautify output markdown
-   [x] ordine di data/alfabetico
    -   [ ] ordine inverso
-   [x] navigazione web: inserimento di solo user e password per accedere al portale polito
-   [x] visualizzazione da terminale
-   [x] flag da shell
-   [x] aggiungere progressbar
-   [x] salvataggio credenziali