import { puppeteer } from "./deps.ts";

const MAIN_URL = "https://idp.polito.it/idp/x509mixed-login";
const EXAM_URL =
  "https://didattica.polito.it/pls/portal30/sviluppo.reg_esami.stugoux2";

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
}

async function scrape() {
  const browser = await puppeteer.launch({
    headless: true,
    args: ["--disable-gpu"],
  });
  const page = await browser.newPage();
  await page.goto(MAIN_URL, { waitUntil: "load" });
  await page.type("#j_username", String(Deno.env.get("USERNAME")));
  await page.type("#j_password", String(Deno.env.get("PASSWORD")));
  await page.keyboard.press("Enter");

  await page.waitForNavigation();
  await page.goto(EXAM_URL);
  await page.waitForNavigation();

  // varibales for results
  const exams: Esame[] = [];
  let ex: string[] = [];
  let codice: string;
  let materia: string;

  const data = await page.$$eval<string[]>(
    "tbody > tr > td",
    (tds) => tds.map((td) => td.innerText.trim()),
  );
  await browser.close();

  data.toString().split(",").forEach((el) => {
    if (el !== "") {
      ex.push(el);
    }

    if (el === "" && ex.length > 0) {
      if (ex.length < 8) {
        ex.unshift(materia);
        ex.unshift(codice);
      }

      const obj = new Esame(ex);

      codice = obj.codice;
      materia = obj.materia;

      exams.push(obj);
      ex = [];
    }
  });

  return exams;
}

// main
const e = await scrape();
console.log(e);
