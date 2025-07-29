// Extracted from: docs\Chapters\12.md
// Original example number: 1
// Auto-generated - do not edit directly

// Basic conditional type syntax
type ConditionalExample<T> = T extends string ? "is string" : "not string"

// Test the conditional type
type Test1 = ConditionalExample<string>  // "is string"
type Test2 = ConditionalExample<number>  // "not string"