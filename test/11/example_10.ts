// Extracted from: docs\Chapters\11.md
// Original example number: 10
// Auto-generated - do not edit directly

type Printer<T> = (value: T) => void

const printString: Printer<string> = str => console.log(str)
const printUnknown: Printer<unknown> = printString // OK