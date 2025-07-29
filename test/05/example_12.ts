// Extracted from: docs\Chapters\05.md
// Original example number: 12
// Auto-generated - do not edit directly

function greet(name = "Guest"): string {
  return `Hello, ${name}`
}

greet() // "Hello, Guest"
greet("Alice") // "Hello, Alice"