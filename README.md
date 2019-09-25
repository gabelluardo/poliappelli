# Poliappelli

Script per ricordare tutte le date degli appelli del PoliTo

### Build

**Richiesti:**

-   python3
-   pipenv
-   make

lanciare la compilazione con `make`

### Uso

    ./script -u sxxxxxx -p xxxxxxxx

Oppure 

    python3 . -u sxxxxxx -p xxxxxxxx

per tutte le opzioni: `./script -h`
```
usage: script [-h] [-u USERNAME] [-p PASSWD] [-s [{Nome,Data,Tipo,Scadenza}]] [-o [OUTPUT]] [-d [DEBUG]] [-m [MESI]]

optional arguments:
-u USERNAME, --user USERNAME            inserimento esplicito dell'username
-p PASSWD, --passwd PASSWD              inserimento esplicito della password (sconsigliato)
-s [{Nome,Data,Tipo,Scadenza}],  
    --sort [{Nome,Data,Tipo,Scadenza}]  ordinamento delle materie (default: Data)
-o [OUTPUT], --output [OUTPUT]          scrive l'output su file (default: esami.md)
-d [DEBUG], --debug [DEBUG]             flag per il parse di 'test.html'
-m [MESI], --mesi [MESI]                range di mesi (default: 12 | non inserito: 4)
```

### Prestazioni

 9,765 secondi + digitazione password


### License

GNU GPL3  
[Geckodriver](https://github.com/mozilla/geckodriver) è software Mozilla sotto MPL

### SO

Linux

--- 

### Doc

-   [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
-   [Selenium](https://selenium-python.readthedocs.io/)
-   [BeautifulTable](https://beautifultable.readthedocs.io/en/latest/index.html)
-   [Argparser](https://docs.python.org/3.6/library/argparse.html#module-argparse)
-   [PyInstaller](https://pyinstaller.readthedocs.io/en/stable/)


### TODO

-   [x] beautify output markdown
-   [x] scriverlo meglio
-   [x] ordine di data/alfabetico
    -   [ ] ordine inverso
-   [x] navigazione web: inserimento di solo user e password per accedere al portale polito
-   [x] visualizzazione da terminale
-   [x] flag da shell
-   [x] aggiungere progressbar
