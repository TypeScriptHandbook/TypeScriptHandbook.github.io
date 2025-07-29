// Extracted from: docs\Chapters\09.md
// Original example number: 3
// Auto-generated - do not edit directly

function print(value: string | number) {
  if (typeof value === "string") {
    console.log(value.toUpperCase()) // narrowed to string
  } else {
    console.log(value.toFixed(2)) // narrowed to number
  }
}