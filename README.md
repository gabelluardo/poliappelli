# Poliappelli

Script per le date degli appelli del PoliTo

### Uso

Necessario installare [deno](https://deno.land/#installation) per eseguire lo script o compilare i sorgenti.

Installare l'eseguibile pupperteer con:

    PUPPETEER_PRODUCT=chrome deno run -A --unstable https://deno.land/x/puppeteer@5.5.1/install.ts

Eseguire lo script con:

    deno run -A --unstable main.ts

Oppure compilare in un binario eseguibile:

    deno compile -A --unstable main.ts

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

### Licenza

GNU GPL3  

--- 

### TODO

*   [ ] beautify output markdown
*   [ ] ordine di data/alfabetico
    -   [ ] ordine inverso
*   [x] navigazione web: inserimento di solo user e password per accedere al portale polito
*   [x] visualizzazione da terminale
*   [ ] flag da shell
*   [ ] aggiungere progressbar
*   [ ] salvataggio credenziali
*   [ ] scrivere i test
