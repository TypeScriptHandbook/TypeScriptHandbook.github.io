// Extracted from: docs\Chapters\05.md
// Original example number: 25
// Auto-generated - do not edit directly

// Using overloads (more verbose):
function process(input: string): string
function process(input: number): number
function process(input: string | number): string | number {
  return typeof input === "string" ? input.toUpperCase() : input * 2
}

// Using union types (simpler):
function process(input: string | number): string | number {
  return typeof input === "string" ? input.toUpperCase() : input * 2
}