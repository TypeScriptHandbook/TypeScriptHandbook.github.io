// Extracted from: docs\Chapters\12.md
// Original example number: 15
// Auto-generated - do not edit directly

type Options = {
  darkMode: boolean
  fontSize: number
}

type PartialOptions = {
  [K in keyof Options]?: Options[K]
}