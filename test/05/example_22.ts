// Extracted from: docs\Chapters\05.md
// Original example number: 22
// Auto-generated - do not edit directly

type Transform<T, U> = (value: T) => U
type Composer = <A, B, C>(f: Transform<B, C>, g: Transform<A, B>) => Transform<A, C>

const compose: Composer = (f, g) => (value) => f(g(value))

const addOne = (x: number) => x + 1
const double = (x: number) => x * 2
const addOneThenDouble = compose(double, addOne)

console.log(addOneThenDouble(3)) // 8 (3 + 1 = 4, then 4 * 2 = 8)