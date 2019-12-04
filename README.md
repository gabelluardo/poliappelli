# Poliappelli

Script per ricordare tutte le date degli appelli del PoliTo

### Build

**Richiesti:**

-   python3
-   pipenv
-   make

### Installazione

    git clone --depth 1 https://gitlab.com/gabelluardo/poliappelli 
    cd poliappelli
    make

Poi sposta `dist/poliappelli` da qualche parte nel tuo `$PATH`

    cd dist/
    mv poliappelli ~/.local/bin

### Uso

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

~10 secondi

### Browser supportati

Firefox
Chromium (WIP)

### SO

Linux  
Windows (non testato)

### Licenza

GNU GPL3  
[Geckodriver](https://github.com/mozilla/geckodriver) è software Mozilla sotto MPL


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