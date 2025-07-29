// Extracted from: docs\Chapters\10.md
// Original example number: 4
// Auto-generated - do not edit directly

let input: string | number = "hello"
input = 42

interface A { a: number }
interface B { b: string }
type AB = A & B

const value: AB = {
  a: 1,
  b: "text"
}