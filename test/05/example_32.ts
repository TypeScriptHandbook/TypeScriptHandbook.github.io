// Extracted from: docs\Chapters\05.md
// Original example number: 32
// Auto-generated - do not edit directly

class EventHandler {
  private count = 0
  
  handleClick() {
    this.count++
    console.log(`Clicked ${this.count} times`)
  }
  
  setup() {
    // Bind the method to preserve `this`
    document.addEventListener("click", this.handleClick.bind(this))
    
    // Or use an arrow function
    document.addEventListener("click", () => this.handleClick())
  }
}