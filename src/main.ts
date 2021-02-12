import { Command, CompletionsCommand, Table } from "../deps.ts";
import { scrape } from "./scraper.ts";
import { VERSION } from "./version.ts";

// define option types
interface Options {
  username: string;
  password: string;
}

// args parser
export class PoliCommand extends Command {
  constructor() {
    super();

    this
      .name("poliappelli")
      .version(VERSION)
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
      .reset();
  }
}

// script runner
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
