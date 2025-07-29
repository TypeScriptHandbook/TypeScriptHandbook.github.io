// Extracted from: docs\Chapters\08.md
// Original example number: 13
// Auto-generated - do not edit directly

function createEnumFromKeys<const T extends readonly string[]>(
  keys: T
): { [K in T[number]]: K } {
  return Object.fromEntries(keys.map(k => [k, k])) as { [K in T[number]]: K }
}