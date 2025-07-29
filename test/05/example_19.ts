// Extracted from: docs\Chapters\05.md
// Original example number: 19
// Auto-generated - do not edit directly

const add: MathOperation = (x, y) => x + y
const multiply: MathOperation = (x, y) => x * y

function applyOperation(op: MathOperation, a: number, b: number): number {
  return op(a, b)
}

const result = applyOperation(multiply, 5, 3) // 15