// Extracted from: docs\Chapters\03.md
// Original example number: 29
// Auto-generated - do not edit directly

type Colors = "red" | "green" | "blue"

const palette = {
  primary: "red",
  secondary: "green",
  accent: "blue"
} satisfies Record<string, Colors>

// palette.primary is still inferred as "red", not Colors