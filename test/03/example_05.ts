// Extracted from: docs\Chapters\03.md
// Original example number: 5
// Auto-generated - do not edit directly

let count = 1
count++ // OK
if (true) {
  let count = 10 // Different variable, shadows outer count
  console.log(count) // 10
}
console.log(count) // 2