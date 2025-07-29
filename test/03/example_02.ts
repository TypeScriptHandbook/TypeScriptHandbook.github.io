// Extracted from: docs\Chapters\03.md
// Original example number: 2
// Auto-generated - do not edit directly

// JavaScript internally rewrites the above as:
function demo() {
  var x // hoisted declaration
  console.log(x) // undefined
  x = 5 // assignment remains here
  console.log(x) // 5
}