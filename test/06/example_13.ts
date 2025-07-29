// Extracted from: docs\Chapters\06.md
// Original example number: 13
// Auto-generated - do not edit directly

type Movable = {
  move(dx: number, dy: number): void
}

class MovablePosition implements Movable {
  constructor(public x: number, public y: number) {}
  move(dx: number, dy: number) {
    this.x += dx
    this.y += dy
  }
}