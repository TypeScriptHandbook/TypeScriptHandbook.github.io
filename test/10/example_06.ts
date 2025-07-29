// Extracted from: docs\Chapters\10.md
// Original example number: 6
// Auto-generated - do not edit directly

// Union of array and function
let mixed: string[] | (() => string)

mixed = ["a", "b"]
console.log(mixed[0]) // "a"

mixed = () => "hello"
console.log(mixed()) // "hello"

interface Metadata {
  description: string
}

// Intersection of function with object type
type CallableWithMeta = Metadata & ((x: number) => number)

const fn: CallableWithMeta = Object.assign(
  (x: number) => x * 2,
  { description: "doubles the input" }
)


console.log(fn(5)) // 10
console.log(fn.description) // "doubles the input"