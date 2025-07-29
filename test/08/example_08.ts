// Extracted from: docs\Chapters\08.md
// Original example number: 8
// Auto-generated - do not edit directly

// Not valid; doesn't create a runtime enum
type MyEnum = {
    [K in 'A' | 'B' | 'C']: K 
}