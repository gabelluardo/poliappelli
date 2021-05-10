import { PoliCommand } from "./src/main.ts";

if (import.meta.main) {
  new PoliCommand().parse(Deno.args);
}
