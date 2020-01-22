# Poliappelli

Script per ricordare tutte le date degli appelli del PoliTo

### Build

**Richiesti:**

-   [poetry](https://python-poetry.org/)

### Installazione

    git clone --depth 1 https://gitlab.com/gabelluardo/poliappelli 
    cd poliappelli
    python3 install.py

Poi sposta `dist/poliappelli` da qualche parte nel tuo `$PATH`, ad esempio:

    cd dist/
    mv poliappelli-xxx-linux64 ~/.local/bin/poliappelli

### Uso

Con poetry:

```
python3 install.py driver
poetry run poliappelli
```

Verrà chiesto di salvare le credenziali in `.login`, per aggiornale: `poliappelli -l`

per tutte le altre opzioni:

```
> poliappelli -h

usage: poliappelli [-h] [-l [LOGIN]] [-s [{Nome,Data,Tipo,Scadenza}]] [-o [FILE]] [-m [MESI]]

optional arguments:
  -h, --help   show this help message and exit
  -l, --login  riscrivere le credenziali nel file .poliappelli
  -s, --sort   ordinamento delle materie (default: Data)
  -o, --out    scrive l'output su file (default: esami.md)
  -m, --mesi   range di mesi (default: 12 | non inserito: 4)
```

### Prestazioni

~7 secondi a 149.32 Mbit/s  
~10 secondi a 0.34 Mbit/s

### Browser supportati

Firefox: usando [Geckodriver](https://github.com/mozilla/geckodriver)  
Chromium (WIP)

### SO

Linux  
Windows (non testato)
MacOS (non testato)

### Licenza

GNU GPL3  

--- 


### TODO

-   [x] beautify output markdown
-   [x] ordine di data/alfabetico
    -   [ ] ordine inverso
-   [x] navigazione web: inserimento di solo user e password per accedere al portale polito
-   [x] visualizzazione da terminale
-   [x] flag da shell
-   [x] aggiungere progressbar
-   [x] salvataggio credenziali
-   [ ] scrivere i test