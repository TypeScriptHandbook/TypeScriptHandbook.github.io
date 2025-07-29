// Extracted from: docs\Chapters\05.md
// Original example number: 24
// Auto-generated - do not edit directly

function getValue(key: "count"): number
function getValue(key: "name"): string
function getValue(key: "active"): boolean
function getValue(key: string): number | string | boolean {
  const config = {
    count: 42,
    name: "TypeScript",
    active: true
  }
  return config[key as keyof typeof config]
}

const count = getValue("count")   // TypeScript knows this is number
const name = getValue("name")     // TypeScript knows this is string
const active = getValue("active") // TypeScript knows this is boolean