// Extracted from: docs\Chapters\10.md
// Original example number: 3
// Auto-generated - do not edit directly

type Position = { x: number; y: number }
type Label = { name: string }

type LabeledPoint = Position & Label

const point: LabeledPoint = {
  x: 10,
  y: 20,
  name: "A"
}