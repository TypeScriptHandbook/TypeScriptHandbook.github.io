// Extracted from: docs\Chapters\04.md
// Original example number: 1
// Auto-generated - do not edit directly

// Method shorthand (ES6)
const person1 = {
  name: "Alice",
  greet() {
    // 'this' refers to the 'person1' object:
    return `Hello, I'm ${this.name}` 
  }
}
console.log(person1.greet()) // Hello, I'm Alice

// Traditional function property
const person2 = {
  name: "Bob",
  greet: function () {
    return `Hello, I'm ${this.name}`
  }
}
console.log(person2.greet()) // Hello, I'm Bob

// Arrow function (not recommended for methods)
const person3 = {
  name: "Charlie",
  greet: () => `Hello, I'm ${this?.name}`
}
console.log(person3.greet()) // Hello, I'm undefined