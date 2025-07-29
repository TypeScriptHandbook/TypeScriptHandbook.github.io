// Extracted from: docs\Chapters\12.md
// Original example number: 19
// Auto-generated - do not edit directly

type PrefixKeys<T> = {
  [K in keyof T as `prefix_${string & K}`]: T[K]
}

// Example:
type Input = { name: string; age: number }
type Prefixed = PrefixKeys<Input>
// { prefix_name: string; prefix_age: number }