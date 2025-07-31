// Extracted from: docs\Chapters\03.md
// Original example number: 3
// Language: JavaScript
// Auto-generated - do not edit directly

function processItems() {
  for (var i = 0; i < 3; i++) {
    setTimeout(() => console.log(i), 100) // Always prints 3!
  }
  console.log(i) // 3 (i leaked out of the loop)
}