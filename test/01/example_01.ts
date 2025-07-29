// Extracted from: docs\Chapters\01.md
// Original example number: 1
// Auto-generated - do not edit directly

type Point2D = { x: number; y: number }

function logPoint(p: Point2D) {
  console.log(`${p.x}, ${p.y}`)
}

const point = { x: 10, y: 20, z: 30 }
logPoint(point) // OK! `z` is just extra