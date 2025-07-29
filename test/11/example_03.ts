// Extracted from: docs\Chapters\11.md
// Original example number: 3
// Auto-generated - do not edit directly

stringArray: Array<string> = ["a", "b"]
const numberPromise: Promise<number> = Promise.resolve(1)

class Container<T> {
  constructor(public value: T) {}

  get(): T {
    return this.value
  }
}

const numberContainer = new Container<number>(123)
console.log(numberContainer.get()) // 123

const stringContainer = new Container("hello")
console.log(stringContainer.get()) // "hello"

// Also works with complex types:
const pointContainer = new Container({ x: 1, y: 2 })
console.log(pointContainer.get().x) // 1