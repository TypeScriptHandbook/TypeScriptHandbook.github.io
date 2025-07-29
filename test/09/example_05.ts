// Extracted from: docs\Chapters\09.md
// Original example number: 5
// Auto-generated - do not edit directly

class Circle {
  radius = 1
}
class Square {
  side = 2
}

// Constructed instances:
const shape: Circle | Square = new Circle()

if (shape instanceof Circle) {
  console.log("Constructed Circle with radius", shape.radius)
} else {
  console.log("Constructed Square with side", shape.side)
}

// Non-constructed objects with the same shape:
const pseudoShape = { radius: 10 }
console.log(pseudoShape instanceof Circle) // false