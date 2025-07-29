// Extracted from: docs\Chapters\07.md
// Original example number: 4
// Auto-generated - do not edit directly

const names = ["Alice", "Bob", "Carol"]

const flattened = names.flatMap((name) => name.split(""))
console.log(flattened) // ['A', 'l', 'i', 'c', 'e', 'B', 'o', 'b']

const found = names.find((name) => name.length > 3)
console.log(found) // "Alice"

function isShortName(value: string): value is string {
  return value.length <= 3
}

const shortNames = names.filter(isShortName)
console.log(shortNames) // ["Bob"]

const hasShort = names.some(isShortName)
console.log(hasShort) // true if any name is short

const allShort = names.every(isShortName)
console.log(allShort) // true if all names are short

const sorted = [...names].sort((a, b) => a.localeCompare(b))
console.log(sorted) // alphabetically sorted copy

// Traverse the array with a for...of loop:
for (const name of names) {
  console.log(name.toUpperCase())
}