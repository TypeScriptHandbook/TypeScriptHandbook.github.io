// Extracted from: docs\Chapters\11.md
// Original example number: 1
// Auto-generated - do not edit directly

function identity<T>(value: T): T {
  return value
}

const a = identity("hello")  // a: string
const b = identity(42)       // b: number