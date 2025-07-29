// Extracted from: docs\Chapters\05.md
// Original example number: 15
// Auto-generated - do not edit directly

function sum(...values: number[]): number {
  return values.reduce((total, value) => total + value, 0)
}

sum(1, 2, 3) // 6
sum(10, 20, 30, 40) // 100