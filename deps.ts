import "https://deno.land/x/dotenv/load.ts";

import { wait } from "https://deno.land/x/wait@0.1.10/mod.ts";
import puppeteer from "https://deno.land/x/puppeteer@5.5.1/mod.ts";
import { Command } from "https://deno.land/x/cliffy@v0.17.2/command/mod.ts";
import { Table } from "https://deno.land/x/cliffy@v0.17.2/table/mod.ts";

export { Command, puppeteer, Table, wait };
