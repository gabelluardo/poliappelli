# Poliappelli

Script per ricordare tutte le date degli appelli del PoliTo

### Build

Per creare un singolo eseguibile nella cartella dist/  
`pyinstaller --oneline script.py`

### Utili

Fare riferimento a:

-   [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) per parsificare le table
-   [Selenium](https://www.seleniumhq.org/) per navigazione web
-   [Getpass](https://alektos.blogspot.com/2011/06/inserire-password-con-python.html) per nascondere le password
-   [BeautifulTable](https://beautifultable.readthedocs.io/en/latest/index.html) per l'output della tabella
-   [Argparser](https://docs.python.org/3.6/library/argparse.html#module-argparse) per i flag da shell
-   [PyInstaller](https://pyinstaller.readthedocs.io/en/stable/)

### TODO

-   [x] beautify output markdown
-   [ ] import automatico su notable
-   [x] scriverlo meglio
-   [x] ordine di data/alfabetico
    -   [ ] ordine inverso
-   [ ] navigazione web: inserimento di solo user e password per accedere al portale polito
-   [x] visualizzazione da terminale
-   [ ] memorizzazione utente. (salvare password???)
-   [x] flag da shell
