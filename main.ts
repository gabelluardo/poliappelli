import { Command, Table } from "./deps.ts";
import { scrape } from "./scraper.ts";

// args parser
const { options } = await new Command()
  .name("poliappelli")
  .version("0.1.0")
  .description("Script per le date degli appelli del PoliTo")
  .option("-u, --username [username:string]", "Login username", {
    default: Deno.env.get("USERNAME"),
  })
  .option("-p, --password [password:string]", "Login password", {
    default: Deno.env.get("PASSWORD"),
  })
  .parse(Deno.args);

// TODO: Prompt input username and password

const list = await scrape(options.username, options.password);

list.sort((a, b) => a.expireDate() - b.expireDate());

new Table()
  .header(list[0].keys())
  .body(list.map((e) => e.values()))
  .maxColWidth(15)
  .padding(1)
  .border(true)
  .render();
