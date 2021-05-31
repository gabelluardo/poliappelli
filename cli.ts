import { PoliCommand } from "./src/main.ts";

if (import.meta.main) {
  const main = new PoliCommand();
  main.parse(Deno.args);
}
