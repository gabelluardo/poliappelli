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
Usage:   poliappelli
Version: v0.1.0     

Description:

  Script per le date degli appelli del PoliTo

Options:

  -h, --help                  - Show this help.
  -V, --version               - Show the version number for this program.
  -u, --username  [username]  - Login username
  -p, --password  [password]  - Login password
```

### Licenza

GNU GPL3

---

### TODO

* [x] beautify output markdown
* [ ] ordine di data/alfabetico
* [x] navigazione web: inserimento di solo user e password per accedere al  portale polito
* [x] visualizzazione da terminale
* [x] aggiungere progressbar
* [ ] salvataggio credenziali
* [ ] export su file
