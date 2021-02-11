import { OptionType } from "https://deno.land/x/cliffy@v0.17.2/flags/types.ts";
import { Command, CompletionsCommand, Table } from "./deps.ts";
import { scrape } from "./scraper.ts";

// define option types
interface Options {
  username: string;
  password: string;
}

// args parser
new Command()
  .name("poliappelli")
  .version("0.1.0")
  .description("Script per le date degli appelli del PoliTo")
  .option("-u, --username [username:string]", "Login username", {
    required: true,
    default: Deno.env.get("POLI_USER"),
  })
  .option("-p, --password [password:string]", "Login password", {
    required: true,
    default: Deno.env.get("POLI_PASS"),
  })
  .action(async (options) => await run(options))
  .command("completions", new CompletionsCommand())
  .parse(Deno.args);

async function run(options: Options) {
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
}
