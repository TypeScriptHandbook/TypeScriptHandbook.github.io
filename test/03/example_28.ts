// Extracted from: docs\Chapters\03.md
// Original example number: 28
// Language: TypeScript
// Auto-generated - do not edit directly

function isString(value: unknown): value is string {
  return typeof value === "string"
}

function processValue(value: unknown): void {
  if (isString(value)) {
    console.log(value.toUpperCase()) // TypeScript knows value is string
  }
}