// Extracted from: docs\Chapters\05.md
// Original example number: 29
// Auto-generated - do not edit directly

class Timer {
  private count = 0
  
  start() {
    // Arrow function preserves `this` from the Timer instance
    setInterval(() => {
      this.count++
      console.log(`Count: ${this.count}`)
    }, 1000)
  }
}