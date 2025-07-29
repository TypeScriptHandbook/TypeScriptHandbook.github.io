// Extracted from: docs\Chapters\11.md
// Original example number: 11
// Auto-generated - do not edit directly

type Handler = (event: MouseEvent) => void

const handleUI: Handler = (event: UIEvent) => {
  // Error in strictFunctionTypes: UIEvent not assignable to MouseEvent
}