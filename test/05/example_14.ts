// Extracted from: docs\Chapters\05.md
// Original example number: 14
// Auto-generated - do not edit directly

// These are equivalent:
function greet1(name: string = "Guest"): string { return `Hello, ${name}` }
function greet2(name?: string): string { return `Hello, ${name || "Guest"}` }