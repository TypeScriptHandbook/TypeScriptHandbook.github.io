Every _function_ in JavaScript is an object.
Regular top-level functions (not arrow functions or methods) each have a default `.prototype` property:

```ts
function greet(name) {
  return `Hello, ${name}`
}

console.log(greet("Alice")) // Hello, Alice

console.log(typeof greet) // "function"
console.log(greet.prototype) // { constructor: [Function: greet] }

const instance = new greet() // TypeError: greet is not a constructor
```

This is different from the function’s own prototype (as in `Object.getPrototypeOf(fn)`); 
it is instead the object that will be assigned as the `[[Prototype]]` of any instance created using `new`.

```js
function Thing() {}
console.log(typeof Thing.prototype) // "object"
console.log(Thing.prototype.constructor === Thing) // true
```

The prototype is used only when you invoke the function with `new`, to assign as the new object's internal prototype (`[[Prototype]]`).

Classes have prototypes associated with their constructors:

```js
function Car(make, model) {
  this.make = make
  this.model = model
}

Car.prototype.describe = function () {
  return `${this.make} ${this.model}`
}

const c = new Car("Toyota", "Camry")

console.log(c.describe()) // Toyota Camry
console.log(c instanceof Car) // true
console.log(Car.prototype) // Car: {}
console.log(Object.getPrototypeOf(c)) // Car: {}
console.log(Object.getPrototypeOf(c) === Car.prototype) // true
console.log(typeof c.prototype) // undefined
```

`Car.prototype` is the object assigned as the prototype of instances created using `new greet()`.

Only functions intended as constructors have a `.prototype` property. 
The `.prototype` is a property on `Car`, not on `c`.

Instances created with `new` do not have a `.prototype` property.
Instead, their internal `[[Prototype]]` (visible via `Object.getPrototypeOf(instance)`) points to the constructor's `.prototype`.

Arrow functions do not have a `.prototype` property:

```js
const arrow = () => {}
console.log(arrow.prototype) // undefined
```

Methods (defined inside objects or classes) also do not have their own `.prototype` property:

```js
const obj = {
  method() {}
}
console.log(obj.method.prototype) // undefined
```

