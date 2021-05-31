# Poliappelli

Script per le date degli appelli del PoliTo

[![vr scripts](https://badges.velociraptor.run/flat.svg)](https://velociraptor.run)

## Uso

Necessario installare [deno](https://deno.land/#installation) per eseguire lo script o compilare i sorgenti.

Eseguire lo script con:

    deno run -A --unstable --lock=lock.json -fn poliappelli https://raw.githubusercontent.com/gabelluardo/poliappelli/main/cli.ts

Oppure installare come script deno:

    deno install -A --unstable --lock=lock.json -fn poliappelli https://raw.githubusercontent.com/gabelluardo/poliappelli/main/cli.ts

Oppure compilare in un binario eseguibile (questa funzione è ancora [sperimentale](https://deno.land/manual/tools/compiler)):

    deno compile -A --unstable --lock=lock.json -o poliappelli https://raw.githubusercontent.com/gabelluardo/poliappelli/main/cli.ts

Potrebbe essere necessario installare l'eseguibile pupperteer con:

    PUPPETEER_PRODUCT=chrome deno run -A --unstable https://deno.land/x/puppeteer@9.0.0/install.ts

## Helper

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
  -o, --output    [file]      - Export file
  -s, --sort                  - Reversed sort by date

Environment variables:

  POLI_USER  <username>  - Username as env var stored in .bashrc
  POLI_PASS  <password>  - Password as env var stored in .bashrc
```

## Author

**poliappelli** © [gabelluardo](https://github.com/gabelluardo)  
Released under the [AGPL3](https://github.com/gabelluardo/poliappelli/blob/master/LICENSE) License.
