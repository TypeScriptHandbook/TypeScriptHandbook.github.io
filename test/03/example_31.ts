// Extracted from: docs\Chapters\03.md
// Original example number: 31
// Language: TypeScript
// Auto-generated - do not edit directly

type Partial<T> = {
  [K in keyof T]?: T[K]
}

type PartialUser = Partial<User>
// All properties become optional