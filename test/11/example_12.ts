// Extracted from: docs\Chapters\11.md
// Original example number: 12
// Auto-generated - do not edit directly

type Box<T> = { value: T }

let numberBox: Box<number> = { value: 42 }
// let stringBox: Box<string> = numberBox // Error: Box<string> not assignable to Box<number>