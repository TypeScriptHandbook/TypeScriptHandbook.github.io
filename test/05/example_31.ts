// Extracted from: docs\Chapters\05.md
// Original example number: 31
// Auto-generated - do not edit directly

class Calculator {
  private result = 0
  
  add(value: number) {
    this.result += value
    return this
  }
  
  multiply(value: number) {
    this.result *= value
    return this
  }
  
  getValue() {
    return this.result
  }
}

const calc = new Calculator()
const result = calc.add(5).multiply(2).getValue() // 10