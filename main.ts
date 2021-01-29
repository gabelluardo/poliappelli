import { Command } from "./deps.ts";
import { scrape } from "./scraper.ts";

// args parser
const { options } = await new Command()
  .name("poliappelli")
  .version("0.1.0")
  .description("Script per le date degli appelli del PoliTo")
  .option("-u, --username [username:string];", "Login username", {
    default: Deno.env.get("USERNAME"),
  })
  .option("-p, --password [password:string];", "Login password", {
    default: Deno.env.get("PASSWORD"),
  })
  .parse(Deno.args);

// main
const e = await scrape(options);
console.log(e);
