// Extracted from: docs\Chapters\11.md
// Original example number: 6
// Auto-generated - do not edit directly

type Response<T = string> = {
  data: T
}

const r1: Response = { data: "ok" }          // uses default string
const r2: Response<number> = { data: 200 }   // overrides default