// Extracted from: docs\Chapters\12.md
// Original example number: 5
// Auto-generated - do not edit directly

type ArgumentType<T> = T extends (arg: infer A) => any ? A : never

type Fn = (x: boolean) => void
type Arg = ArgumentType<Fn>  // boolean