// Extracted from: docs\Chapters\12.md
// Original example number: 4
// Auto-generated - do not edit directly

type ElementType<T> = T extends (infer U)[] ? U : T

// Usage:
type TestArray = ElementType<string[]>   // string
type TestPrimitive = ElementType<number> // number