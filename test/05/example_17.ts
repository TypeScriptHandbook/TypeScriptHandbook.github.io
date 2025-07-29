// Extracted from: docs\Chapters\05.md
// Original example number: 17
// Auto-generated - do not edit directly

function createRecord<T>(id: string, ...data: T[]): Record<string, T[]> {
  return { [id]: data }
}

const userRecord = createRecord("users", "Alice", "Bob", "Charlie")
// { users: ["Alice", "Bob", "Charlie"] }