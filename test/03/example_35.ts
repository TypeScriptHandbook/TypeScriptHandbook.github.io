// Extracted from: docs\Chapters\03.md
// Original example number: 35
// Language: TypeScript
// Auto-generated - do not edit directly

function findFirstEven(numbers: number[]): number | undefined {
  for (const num of numbers) {
    if (num % 2 !== 0) {
      continue // Skip odd numbers
    }
    if (num > 100) {
      break // Stop if we find a large even number
    }
    return num // Return first small even number
  }
  return undefined
}