import { puppeteer, Spinner } from "./deps.ts";

// deno-fmt-ignore
const EXAM_URL = "https://didattica.polito.it/pls/portal30/sviluppo.reg_esami.stugoux2";
const MAIN_URL = "https://idp.polito.it/idp/x509mixed-login";

class Esame {
  public codice: string;
  public materia: string;
  public data: string;
  public aula: string;
  public tipo: string;
  public insegnante: string;
  public scadenza: string;
  public prenotati: string;

  constructor(ary: string[]) {
    this.codice = ary[0];
    this.materia = ary[1];
    this.data = ary[2];
    this.aula = ary[3];
    this.tipo = ary[4];
    this.insegnante = ary[5];
    this.scadenza = ary[6];
    this.prenotati = ary[7];
  }

  keys(): string[] {
    return [
      "Codice",
      "Materia",
      "Data",
      // "Aula",
      // "Tipo",
      "Insegnante",
      "Scadenza",
      "Prenotati",
    ];
  }

  values(): string[] {
    return [
      this.codice,
      this.materia,
      this.data,
      // this.aula,
      // this.tipo,
      this.insegnante,
      this.scadenza,
      this.prenotati,
    ];
  }
}

export async function scrape(options: any) {
  const spinner = Spinner.getInstance();
  await spinner.start("Scraping website");

  const browser = await puppeteer.launch({
    headless: true,
    args: ["--disable-gpu"],
  });
  const page = await browser.newPage();
  await page.goto(MAIN_URL, { waitUntil: "load" });
  await page.type("#j_username", options.username);
  await page.type("#j_password", options.password);
  await page.keyboard.press("Enter");

  await page.waitForNavigation();
  await page.goto(EXAM_URL);
  await page.waitForNavigation();

  const data = await page.$$eval<string[]>(
    "tbody > tr > td",
    (tds) => tds.map((td) => td.innerText.trim()),
  );
  await browser.close();
  await spinner.succeed("Scraping completed");

  // varibales for results
  const exams: Esame[] = [];
  let ex: string[] = [];

  data.toString().split(",").forEach((el) => {
    if (el !== "") {
      ex.push(el);
    }

    if (el === "" && ex.length > 0) {
      if (ex.length < 8) {
        const last = exams[exams.length - 1];
        ex.unshift(last.materia);
        ex.unshift(last.codice);
      }

      const obj = new Esame(ex);

      exams.push(obj);
      ex = [];
    }
  });

  return exams;
}
