// Extracted from: docs\Chapters\12.md
// Original example number: 17
// Auto-generated - do not edit directly

type MyPartial<T> = {
  [P in keyof T]?: T[P]
}

type MyReadonly<T> = {
  readonly [P in keyof T]: T[P]
}

type MyRequired<T> = {
  [P in keyof T]-?: T[P]
}

// Example usage
type User = { name: string; age?: number }
type PartialUser = MyPartial<User>     // { name?: string; age?: number }
type RequiredUser = MyRequired<User>   // { name: string; age: number }
type ReadonlyUser = MyReadonly<User>   // { readonly name: string; readonly age?: number }