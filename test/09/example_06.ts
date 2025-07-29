// Extracted from: docs\Chapters\09.md
// Original example number: 6
// Auto-generated - do not edit directly

type Status = "loading" | "success" | "error"

declare const status: Status

if (status === "success") {
  console.log("Operation successful")
} else if (status === "error") {
  console.log("Operation failed")
}