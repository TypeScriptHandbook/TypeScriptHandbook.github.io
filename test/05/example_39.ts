// Extracted from: docs\Chapters\05.md
// Original example number: 39
// Auto-generated - do not edit directly

// Mutating (less predictable):
function addToList<T>(list: T[], item: T): void {
  list.push(item)
}

// Non-mutating (more predictable):
function addToList<T>(list: readonly T[], item: T): T[] {
  return [...list, item]
}