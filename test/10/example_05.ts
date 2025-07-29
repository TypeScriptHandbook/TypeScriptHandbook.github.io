// Extracted from: docs\Chapters\10.md
// Original example number: 5
// Auto-generated - do not edit directly

type A = { value: string }
type B = { value: number }
type C = A & B

// C is inferred as:
// {
//   value: string & number
// }

// Since no value can be both a string and a number at the same time,
// TypeScript reduces this to `never`:
const impossible: C = { value: 42 } // Error