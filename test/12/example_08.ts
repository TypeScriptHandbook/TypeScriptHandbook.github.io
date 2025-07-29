// Extracted from: docs\Chapters\12.md
// Original example number: 8
// Auto-generated - do not edit directly

// Combine literal types:
type Lang = "en" | "fr"
type FileExtension = ".json" | ".txt"
type Filename = `${Lang}${FileExtension}`

const file: Filename = "en.json" // OK