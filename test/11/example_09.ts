// Extracted from: docs\Chapters\11.md
// Original example number: 9
// Auto-generated - do not edit directly

type ReadOnlyBox<T> = {
  readonly value: T
}

const stringBox: ReadOnlyBox<string> = { value: "hello" }
const widerBox: ReadOnlyBox<string | number> = stringBox // OK