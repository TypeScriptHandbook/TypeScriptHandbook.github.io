// Extracted from: docs\Chapters\10.md
// Original example number: 7
// Auto-generated - do not edit directly

type Circle = {
  kind: "circle"
  radius: number
}

type Square = {
  kind: "square"
  size: number
}

type Shape = Circle | Square

function area(shape: Shape): number {
  switch (shape.kind) {
    case "circle":
      return Math.PI * shape.radius ** 2
    case "square":
      return shape.size * shape.size
  }
}

const c: Shape = { kind: "circle", radius: 3 }
const s: Shape = { kind: "square", size: 4 }

console.log(area(c)) // 28.274333882308138
console.log(area(s)) // 16