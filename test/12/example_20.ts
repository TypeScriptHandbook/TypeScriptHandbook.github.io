// Extracted from: docs\Chapters\12.md
// Original example number: 20
// Auto-generated - do not edit directly

type OnlyStrings<T> = {
  [K in keyof T as T[K] extends string ? K : never]: T[K]
}

// Example:
type Mixed = { a: string; b: number; c: string }
type StringsOnly = OnlyStrings<Mixed>
// { a: string; c: string }