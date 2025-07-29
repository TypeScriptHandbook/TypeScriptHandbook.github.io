// Extracted from: docs\Chapters\12.md
// Original example number: 14
// Auto-generated - do not edit directly

const status = {
  loading: "loading",
  success: "success"
} as const

type Status = typeof status[keyof typeof status] // "loading" | "success"