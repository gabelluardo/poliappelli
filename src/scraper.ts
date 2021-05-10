import puppeteer from "puppeteer";
import Kia from "kia";
import { existsSync } from "fs";

// deno-fmt-ignore
const EXAM_URL = "https://didattica.polito.it/pls/portal30/sviluppo.reg_esami.stugoux2";
const MAIN_URL = "https://idp.polito.it/idp/x509mixed-login";

export const header = [
  "Codice",
  "Materia",
  "Data",
  "Insegnante",
  "Scadenza",
  "Prenotati",
];

interface Exam {
  raw: string[];
  codice: string;
  materia: string;
  data: string;
  aula: string;
  tipo: string;
  insegnante: string;
  scadenza: string;
  prenotati: string;
}

class Exam {
  constructor(str: string[]) {
    this.raw = str.filter((e) => e.length);

    [
      this.codice,
      this.materia,
      this.data,
      ,
      ,
      this.insegnante,
      this.scadenza,
      this.prenotati,
    ] = str;
  }

  expireDate(): number {
    const [d, m, y] = this.scadenza.split("-").map((e) => parseInt(e));
    return new Date(y, m, d).getTime();
  }

  examDate(): number {
    const [d, m, y] = this.data.split("-").map((e) => parseInt(e));
    return new Date(y, m, d).getTime();
  }
}

function purgeData(data: string): Exam[] {
  const dd = data.split(",");
  const d = new Array(Math.ceil(dd.length / 10)).fill([])
    .map((_) => dd.splice(0, 10))
    .map((e) => new Exam(e));

  const exams = d.map((e, id) => {
    if (e.codice === "" || e.materia === "") {
      e.raw = d[id - 1].raw;
      e.codice = d[id - 1].codice;
      e.materia = d[id - 1].materia;
    }
    return e;
  });

  return exams;
}

function findBrowserPath(): string {
  const paths = [
    // Linux
    "/usr/bin/chrome",
    "/usr/bin/chromium",
    "/usr/bin/firefox-nightly",
    // Windows
    "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
  ];

  return paths.filter((p) => existsSync(p))[0];
}

export async function scrape(user: string, pass: string) {
  const browser = await puppeteer.launch({
    executablePath: findBrowserPath(),
  });

  const spinner = new Kia({ text: "Start scraping", color: "green" });
  spinner.start();

  const page = await browser.newPage();
  await page.goto(MAIN_URL, { waitUntil: "load" });
  await page.type("#j_username", user);
  await page.type("#j_password", pass);
  await page.keyboard.press("Enter");

  spinner.set("Insert credentials");

  await page.waitForNavigation();
  await page.goto(EXAM_URL);
  await page.waitForNavigation();

  spinner.set("Parse exams page");

  const data = await page.$$eval<string[]>(
    "tbody > tr > td",
    (tds) => tds.map((td) => td.innerText.trim()),
  );
  await browser.close();

  spinner.succeed("Scraping completed");

  return purgeData(data.toString());
}
