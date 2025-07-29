// Extracted from: docs\Chapters\02.md
// Original example number: 3
// Auto-generated - do not edit directly

function getRandomValue(): unknown {
  return Math.random() > 0.5 ? "hello" : 42
}

let userInput: unknown = getRandomValue()

if (typeof userInput === "string") {
  console.log(userInput.toUpperCase())
}