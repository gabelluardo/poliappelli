# Poliappelli

Script per ricordare tutte le date degli appelli del PoliTo

### Build

Per creare un singolo eseguibile nella cartella dist/  
`pip install --user pyinstaller`  
`pyinstaller --oneline script.py`

### Utili

Fare riferimento a:

-   [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
-   [Selenium](https://selenium-python.readthedocs.io/)
-   [BeautifulTable](https://beautifultable.readthedocs.io/en/latest/index.html)
-   [Argparser](https://docs.python.org/3.6/library/argparse.html#module-argparse)
-   [PyInstaller](https://pyinstaller.readthedocs.io/en/stable/)

### Prestazioni

 9,765 secondi + digitazione password

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
