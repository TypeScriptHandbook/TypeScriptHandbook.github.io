// Extracted from: docs\Chapters\03.md
// Original example number: 4
// Auto-generated - do not edit directly

function processItems() {
  for (let i = 0; i < 3; i++) {
    setTimeout(() => console.log(i), 100) // Prints 0, 1, 2
  }
  // console.log(i) // Error: i is not defined outside the loop
}