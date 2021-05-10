import { Command, CompletionsCommand } from "command";
import { Table } from "table";

import { header, scrape } from "./scraper.ts";
import { VERSION } from "./version.ts";

// define option types
interface Options {
  username: string;
  password: string;
  output?: string;
  sort?: boolean;
}

// args parser
export class PoliCommand extends Command {
  constructor() {
    super();

    this
      .name("poliappelli")
      .version(VERSION)
      .description("Script per le date degli appelli del PoliTo")
      .allowEmpty(false)
      .env(
        "POLI_USER=<username:string>",
        "Username as env var stored in .bashrc",
      )
      .env(
        "POLI_PASS=<password:string>",
        "Password as env var stored in .bashrc",
      )
      .option("-u, --username [username:string]", "Login username", {
        default: Deno.env.get("POLI_USER"),
      })
      .option("-p, --password [password:string]", "Login password", {
        default: Deno.env.get("POLI_PASS"),
      })
      .option(
        "-o, --output [file:string]",
        "Export file",
        (value: string): string =>
          typeof value === "boolean" ? "esami.txt" : value,
      )
      .option("-s, --sort", "Reversed sort by date")
      .action(async (options) => await run(options))
      .command("completions", new CompletionsCommand())
      .reset();
  }
}

async function run(options: Options) {
  // @todo Prompt input username and password

  const list = await scrape(options.username, options.password);

  if (options.sort) {
    // Reversed chronological order
    list.sort((a, b) => b.examDate() - a.examDate());
  } else {
    // Chronological order
    list.sort((a, b) => a.examDate() - b.examDate());
  }

  const table = new Table()
    .header(header)
    .body(list.map((e) => e.raw))
    .maxColWidth(15)
    .padding(1)
    .border(true);

  if (options.output) {
    // Overwrite existet file
    Deno.writeTextFile(options.output, table.toString());
  } else {
    // Print table on screen
    table.render();
  }
}
