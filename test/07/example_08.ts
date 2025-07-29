// Extracted from: docs\Chapters\07.md
// Original example number: 8
// Auto-generated - do not edit directly

type LabeledPair = { label: string; coords: [number, number] }
const point: LabeledPair = { label: "origin", coords: [0, 0] }
const [x, y] = point.coords