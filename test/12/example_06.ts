// Extracted from: docs\Chapters\12.md
// Original example number: 6
// Auto-generated - do not edit directly

type ParametersOf<T> = T extends (...args: infer P) => any ? P : never

type MyFn = (x: string, y: number) => void
type Params = ParametersOf<MyFn>  // [string, number]