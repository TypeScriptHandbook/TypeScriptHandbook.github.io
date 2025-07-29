// Extracted from: docs\Chapters\06.md
// Original example number: 12
// Auto-generated - do not edit directly

interface Printable {
  toString(): string
}

class NamedCoordinate implements Printable {
  constructor(public x: number, public y: number, public label: string) {}
  toString(): string {
    return `${this.label}: (${this.x}, ${this.y})`
  }
}