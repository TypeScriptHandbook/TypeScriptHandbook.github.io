// Extracted from: docs\Chapters\12.md
// Original example number: 22
// Auto-generated - do not edit directly

type NullableFields<T> = {
  [K in keyof T]: null extends T[K] ? T[K] : T[K] | null
}

// Example:
type Person = { name: string; bio: string | null }
type WithNullable = NullableFields<Person>
// { name: string | null; bio: string | null }