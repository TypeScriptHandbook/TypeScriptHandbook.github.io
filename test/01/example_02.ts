// Extracted from: docs\Chapters\01.md
// Original example number: 2
// Auto-generated - do not edit directly

type Point2D = { x: number; y: number }

function logPoint(p: Point2D) {
  console.log(`${p.x}, ${p.y}`)
}

const coordinates = { x: 10, y: 20, z: 30 }
logPoint(coordinates) // OK! `z` is just extra