// Extracted from: docs\Chapters\08.md
// Original example number: 10
// Auto-generated - do not edit directly

export const MyEnum = {
  A: 'A',
  B: 'B',
  C: 'C'
} as const

export type MyEnum = keyof typeof MyEnum // "A" | "B" | "C"
export type MyEnumValue = typeof MyEnum[MyEnum] // "A" | "B" | "C"