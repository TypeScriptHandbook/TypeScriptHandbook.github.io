// Extracted from: docs\Chapters\08.md
// Original example number: 15
// Auto-generated - do not edit directly

function createEnumFromKeys<const T extends readonly string[]>(
  keys: T
): { readonly [K in T[number]]: K } {
  const result = Object.fromEntries(keys.map(k => [k, k])) as {
    [K in T[number]]: K
  }
  return result as const
}