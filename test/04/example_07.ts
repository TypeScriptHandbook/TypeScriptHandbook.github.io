// Extracted from: docs\Chapters\04.md
// Original example number: 7
// Auto-generated - do not edit directly

type Point = { x: number; y: number };

class Circle {
  constructor(public center: Point, public radius: number) {}
  
  area(): number {
    return Math.PI * this.radius ** 2;
  }
}

const circle = new Circle({ x: 2, y: 2 }, 7);