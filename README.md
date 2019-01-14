# Poliappelli

Script per ricordare tutte le date degli appelli del PoliTo

### Build

Per creare un singolo eseguibile nella cartella dist/  
`pip install --user pyinstaller`  
`pyinstaller --oneline script.py`

### Utili

Fare riferimento a:

-   [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) per parsificare le table
-   [Selenium](https://selenium-python.readthedocs.io/) per navigazione web
-   [BeautifulTable](https://beautifultable.readthedocs.io/en/latest/index.html) per l'output della tabella
-   [Argparser](https://docs.python.org/3.6/library/argparse.html#module-argparse) per i flag da shell
-   [PyInstaller](https://pyinstaller.readthedocs.io/en/stable/)

### Prestazioni

20,110s secondi + digitazione password

### TODO

-   [x] beautify output markdown
-   [ ] import automatico su notable
-   [x] scriverlo meglio
-   [x] ordine di data/alfabetico
    -   [ ] ordine inverso
-   [x] navigazione web: inserimento di solo user e password per accedere al portale polito
-   [x] visualizzazione da terminale
-   [ ] memorizzazione utente. (salvare password??? NO)
-   [x] flag da shell
-   [ ] aggiungere progressbar
