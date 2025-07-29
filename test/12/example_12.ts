// Extracted from: docs\Chapters\12.md
// Original example number: 12
// Auto-generated - do not edit directly

type ValueOf<T> = T[keyof T]
type PersonValues = ValueOf<Person> // string | number