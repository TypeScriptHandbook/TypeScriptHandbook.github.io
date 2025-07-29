// Extracted from: docs\Chapters\06.md
// Original example number: 26
// Auto-generated - do not edit directly

interface SafeConfig {
  mode: string
  [key: string]: string // OK: 'mode' is a string
}

interface UnsafeConfig {
  debug: boolean
  [key: string]: string // Error: 'debug' is boolean, not string
}