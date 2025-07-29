// Extracted from: docs\Chapters\06.md
// Original example number: 1
// Auto-generated - do not edit directly

class Point {
  // Constructor shorthand automatically defines and assigns fields
  constructor(public x: number, public y: number) {}
  toString(): string {
    return `(${this.x}, ${this.y})`
  }
}