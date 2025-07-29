// Extracted from: docs\Chapters\12.md
// Original example number: 3
// Auto-generated - do not edit directly

type A = { kind: "A" }
type B = { kind: "B" }

type SelectType<T> = T extends string ? A : B

function create<T>(value: T): SelectType<T> {
  return (typeof value === "string"
    ? { kind: "A" }
    : { kind: "B" }) as SelectType<T>
}

const resultString = create("hello") // type A
const resultNumber = create(123)     // type B
console.log(resultString) // { kind: "A" }
console.log(resultNumber) // { kind: "B" }