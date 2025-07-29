// Extracted from: docs\Chapters\06.md
// Original example number: 9
// Auto-generated - do not edit directly

class SecretPoint {
  constructor(private x: number, private y: number) {}
  reveal(): string {
    return `(${this.x}, ${this.y})`
  }
}