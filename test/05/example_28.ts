// Extracted from: docs\Chapters\05.md
// Original example number: 28
// Auto-generated - do not edit directly

const user = {
  name: "Alice",
  greet: () => {
    return `Hello, I'm ${this.name}` // `this` refers to outer scope, not user
  }
}

console.log(user.greet()) // "Hello, I'm undefined"