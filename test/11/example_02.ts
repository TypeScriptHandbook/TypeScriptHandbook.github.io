// Extracted from: docs\Chapters\11.md
// Original example number: 2
// Auto-generated - do not edit directly

type Box<T> = {
  value: T
}

const stringBox: Box<string> = { value: "wrapped" }
const numberBox: Box<number> = { value: 99 }