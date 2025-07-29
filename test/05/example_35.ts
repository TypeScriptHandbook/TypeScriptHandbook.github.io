// Extracted from: docs\Chapters\05.md
// Original example number: 35
// Auto-generated - do not edit directly

// void functions can return undefined, but callers shouldn't use the result
const voidFn = (): void => {
  return undefined // OK
}

const result1 = voidFn() // result1 has type void (not useful)

// undefined functions explicitly return undefined as a value
const undefinedFn = (): undefined => {
  return undefined // Required
}

const result2 = undefinedFn() // result2 has type undefined (can be checked)

if (result2 === undefined) {
  // This check makes sense
}