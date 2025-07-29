// Extracted from: docs\Chapters\08.md
// Original example number: 9
// Auto-generated - do not edit directly

const keys = ['A', 'B', 'C'] as const
type MyEnum = (typeof keys)[number] // "A" | "B" | "C"

const MyEnumValues: { [K in MyEnum]: K } = Object.fromEntries(
  keys.map(k => [k, k])
) as { [K in MyEnum]: K }