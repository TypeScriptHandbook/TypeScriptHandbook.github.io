// Extracted from: docs\Chapters\07.md
// Original example number: 12
// Auto-generated - do not edit directly

const keywords: readonly string[] = ["async", "await"]

const locked = ["on", "off"] as const
// locked has type: readonly ["on", "off"]

const response = { status: "OK", code: 200 } as const
// response.status is type "OK", not string
// response.code is type 200, not number

function logKeywords(values: readonly string[]) {
  values.forEach(console.log)
  // values.push("new") // Error: cannot modify a readonly array
}

logKeywords(keywords)