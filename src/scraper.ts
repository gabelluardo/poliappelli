import { existsSync, Kia, puppeteer } from "../deps.ts";

// deno-fmt-ignore
const EXAM_URL = "https://didattica.polito.it/pls/portal30/sviluppo.reg_esami.stugoux2";
const MAIN_URL = "https://idp.polito.it/idp/x509mixed-login";

export const header = [
  "Codice",
  "Materia",
  "Data",
  "Sede",
  "Tipo",
  "Insegnante",
  "Scadenza",
  "Prenotati",
];

interface Exam {
  raw: string[];
  codice: string;
  materia: string;
  data: string;
  sede: string;
  tipo: string;
  insegnante: string;
  scadenza: string;
  prenotati: string;
}

class Exam {
  constructor(str: string[]) {
    this.raw = str.filter((e) => e);

    [
      this.codice,
      this.materia,
      this.data,
      this.sede,
      this.tipo,
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

  static from(str: string[]): Exam {
    return new Exam(str);
  }
}

function purgeData(str: string): Exam[] {
  const rawData = str.split(",").map((s) => s.trim());
  const data = new Array(Math.ceil(rawData.length / 9))
    .fill([])
    .map((_) => rawData.splice(0, 9))
    .map((e) => Exam.from(e));

  const exams = data.map((e) => {
    if (!e.codice || !e.materia) {
      const ex = data.find((ex) => ex.insegnante === e.insegnante);

      e.codice = ex?.codice || "";
      e.materia = ex?.materia || "";
      e.raw = [e.codice, e.materia, ...e.raw];
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

  spinner.set("Inserting credentials");

  await page.waitForNavigation();
  await page.goto(EXAM_URL);
  await page.waitForNavigation();

  spinner.set("Parsing exams page");

  const data = await page.$$eval<string[]>(
    "tbody > tr > td",
    (tds) => tds.map((td) => td.innerText).filter((s) => s),
  );
  await browser.close();

  spinner.succeed("Scraping completed");

  return purgeData(data.toString());
}
