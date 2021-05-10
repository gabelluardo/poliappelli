import { assert } from "testing/asserts.ts";

const { test } = Deno;

test({
  name: "prova",
  fn(): void {
    assert(true);
  },
});
