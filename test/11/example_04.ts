// Extracted from: docs\Chapters\11.md
// Original example number: 4
// Auto-generated - do not edit directly

function lengthOf<T extends { length: number }>(value: T): number {
  return value.length
}

lengthOf("hello")        // 5
lengthOf([1, 2, 3])       // 3
// lengthOf(42)          // Error: number doesn't have a length