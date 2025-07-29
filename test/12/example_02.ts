// Extracted from: docs\Chapters\12.md
// Original example number: 2
// Auto-generated - do not edit directly

type IsString<T> = T extends string ? true : false
type A = IsString<string>  // true
type B = IsString<number>  // false