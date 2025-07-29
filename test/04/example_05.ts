// Extracted from: docs\Chapters\04.md
// Original example number: 5
// Auto-generated - do not edit directly

const user = {
  name: "Sam",
  greet() {
    return `Hello, ${this.name}`
  }
}

const greetRef = user.greet
console.log(greetRef()) // Hello, undefined