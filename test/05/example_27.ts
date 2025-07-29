// Extracted from: docs\Chapters\05.md
// Original example number: 27
// Auto-generated - do not edit directly

const user = {
  name: "Alice",
  greet() {
    return `Hello, I'm ${this.name}`
  }
}

console.log(user.greet()) // "Hello, I'm Alice"

const greetFn = user.greet
console.log(greetFn()) // "Hello, I'm undefined" (this is lost)