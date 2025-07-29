// Extracted from: docs\Chapters\10.md
// Original example number: 8
// Auto-generated - do not edit directly

function area(shape: Shape): number {
  switch (shape.kind) {
    case "circle":
      return Math.PI * shape.radius ** 2
    case "square":
      return shape.size * shape.size
    default:
      const _exhaustiveCheck: never = shape
      return _exhaustiveCheck
  }
}