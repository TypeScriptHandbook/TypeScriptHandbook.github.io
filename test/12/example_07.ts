// Extracted from: docs\Chapters\12.md
// Original example number: 7
// Auto-generated - do not edit directly

type Flatten<T> = T extends (infer U)[] ? Flatten<U> : T

type NestedArray = number[][][]
type FlatType = Flatten<NestedArray>  // number