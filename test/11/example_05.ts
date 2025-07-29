// Extracted from: docs\Chapters\11.md
// Original example number: 5
// Auto-generated - do not edit directly

interface HasId<T extends { id: number }> {
  item: T
}

const record: HasId<{ id: number; name: string }> = {
  item: { id: 1, name: "Item" }
}