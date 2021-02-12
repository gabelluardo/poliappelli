import { puppeteer, wait } from "../deps.ts";

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

  expireDate(): number {
    const [d, m, y] = this.scadenza.split("-").map((e) => parseInt(e));
    return new Date(y, m, d).getTime();
  }

  examDate(): number {
    const [d, m, y] = this.data.split("-").map((e) => parseInt(e));
    return new Date(y, m, d).getTime();
  }
}

export async function scrape(user: string, pass: string) {
  const spinner = wait("Start scraping").start();

  const browser = await puppeteer.launch({
    headless: true,
    args: ["--disable-gpu"],
  });
  const page = await browser.newPage();
  await page.goto(MAIN_URL, { waitUntil: "load" });
  await page.type("#j_username", user);
  await page.type("#j_password", pass);
  await page.keyboard.press("Enter");

  spinner.text = "Insert credentials";

  await page.waitForNavigation();
  await page.goto(EXAM_URL);
  await page.waitForNavigation();

  spinner.text = "Parse exams page";

  const data = await page.$$eval<string[]>(
    "tbody > tr > td",
    (tds) => tds.map((td) => td.innerText.trim()),
  );
  await browser.close();

  spinner.succeed("Scraping completed");
  //spinner.stop();

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
