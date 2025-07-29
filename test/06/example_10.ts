// Extracted from: docs\Chapters\06.md
// Original example number: 10
// Auto-generated - do not edit directly

class Animal {
  constructor(public name: string) {}
  speak(): void {
    console.log(`${this.name} makes a sound.`)
  }
}

class Dog extends Animal {
  speak(): void {
    console.log(`${this.name} barks.`)
  }
}

// Upcasting and dynamic binding
const a: Animal = new Dog("Rover")
a.speak() // "Rover barks."