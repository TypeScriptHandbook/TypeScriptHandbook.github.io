// Extracted from: docs\Chapters\12.md
// Original example number: 18
// Auto-generated - do not edit directly

type FullyMutable<T> = {
  -readonly [P in keyof T]-?: T[P]
}