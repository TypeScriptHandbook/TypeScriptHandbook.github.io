// Extracted from: docs\Chapters\11.md
// Original example number: 7
// Auto-generated - do not edit directly

function wrap<T>(value: T): { value: T } {
  return { value }
}

const result = wrap("hello")  // inferred as string

// But inference is shallow:
const complex = wrap({ x: 1 })
// complex.value.x inferred as number, but not deeply readonly