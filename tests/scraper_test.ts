import { assert } from "../deps.ts";

const { test } = Deno;

test({
  name: "prova",
  fn(): void {
    assert(true);
  },
});
