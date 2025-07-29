// Extracted from: docs\Chapters\10.md
// Original example number: 1
// Auto-generated - do not edit directly

type Status = "loading" | "success" | "error"

let current: Status = "loading"
current = "success" // OK
current = "done" // Error: not assignable to Status