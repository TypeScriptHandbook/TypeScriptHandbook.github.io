// Extracted from: docs\Chapters\05.md
// Original example number: 34
// Auto-generated - do not edit directly

function findItem<T>(items: T[], predicate: (item: T) => boolean): T | undefined {
  for (const item of items) {
    if (predicate(item)) {
      return item
    }
  }
  return undefined // Explicit return of undefined
}

// The return type clearly shows undefined is a possible outcome
const user = findItem(users, u => u.id === 123) // User | undefined