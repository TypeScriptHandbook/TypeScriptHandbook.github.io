// Extracted from: docs\Chapters\03.md
// Original example number: 18
// Language: TypeScript
// Auto-generated - do not edit directly

console.log(5 == "5")  // true (type coercion)
console.log(5 === "5") // false (strict equality)

// Always prefer strict equality
function isValidId(id: unknown): id is number {
  return typeof id === "number" && id > 0
}