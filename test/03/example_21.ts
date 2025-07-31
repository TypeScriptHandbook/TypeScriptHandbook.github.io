// Extracted from: docs\Chapters\03.md
// Original example number: 21
// Language: TypeScript
// Auto-generated - do not edit directly

const user = { name: "Alice", age: 30, email: "alice@example.com" }
const { name, ...otherProps } = user

const numbers = [1, 2, 3, 4, 5]
const [first, second, ...rest] = numbers