// Extracted from: docs\Chapters\06.md
// Original example number: 11
// Auto-generated - do not edit directly

abstract class Shape {
  constructor(public color: string) {}
  abstract area(): number
  describe(): string {
    return `A ${this.color} shape.`
  }
}

class Square extends Shape {
  constructor(color: string, public size: number) {
    super(color)
  }
  area(): number {
    return this.size * this.size
  }
}