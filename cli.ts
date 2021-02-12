import { PoliCommand } from "./src/main.ts";

// TODO: Rimuove supporto ai .env
import "https://deno.land/x/dotenv/load.ts";

if (import.meta.main) {
  new PoliCommand().parse(Deno.args);
}
