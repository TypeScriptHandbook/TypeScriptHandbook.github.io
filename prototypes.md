## The JavaScript Prototype Model

JavaScript’s object system is fundamentally different from classical object-oriented languages.
At its core, JavaScript uses *prototype-based inheritance*, and understanding how constructors and prototypes work together is essential to mastering the language.
Understanding how JavaScript handles constructors and prototypes is crucial for working effectively with its object model.

Constructors are simply functions invoked with `new`, and the `.prototype` property provides a shared mechanism for inheritance.
By mastering how prototypes link instances and support shared behavior, 
you gain a deep understanding of JavaScript’s core object system and how features like classes are built on top of it.

### The Prototype Property

Every function in JavaScript has a `prototype` property by default.
This is an object that becomes the prototype of any instance created using that function as a constructor.

The `prototype` serves as the *shared space for instance methods and properties*.
Rather than duplicating methods for every instance, JavaScript allows all instances to delegate behavior to this shared prototype object.

```js
Car.prototype.describe = function() {
  return `${this.make} ${this.model}`;
};

console.log(myCar.describe()); // "Toyota Camry"
```

#### When Does a Function Get a Prototype?

A function gets a `.prototype` property *as soon as it is defined*.
This happens whether the function is ever used as a constructor.
It's simply part of how JavaScript sets up normal functions.

```js
function regularFunction() {}
console.log(typeof regularFunction.prototype); // "object"
```

Note: this does *not* apply to arrow functions.

```js
const arrow = () => {};
console.log(arrow.prototype); // undefined
```

Arrow functions do not get a `.prototype` because they are not designed to be used with `new`.

Every function in JavaScript has a `prototype` property by default.
This is an object that becomes the prototype of any instance created using that function as a constructor.

The `prototype` serves as the shared space for instance methods and properties.
Rather than duplicating methods for every instance, JavaScript allows all instances to delegate behavior to this shared prototype object.

```js
Car.prototype.describe = function() {
  return `${this.make} ${this.model}`;
};

console.log(myCar.describe()); // "Toyota Camry"
```

### Shared Prototypes Across Instances

All objects created from the same constructor share the same prototype.
This means they all have access to the same methods without duplicating them.

```js
const car1 = new Car("Honda", "Accord");
const car2 = new Car("Ford", "Focus");

console.log(car1.describe()); // "Honda Accord"
console.log(car2.describe()); // "Ford Focus"
console.log(car1.describe === car2.describe); // true
```

### Constructors vs. Regular Functions

In JavaScript, a *constructor* is simply a function used to create new objects.
What makes a function a constructor isn’t its declaration, but how it is called.
When a function is invoked with the `new` keyword, it acts as a constructor.

Here's what happens when a function is called with `new`:

1. A new empty object is created.
2. That object’s prototype is set to the function’s `.prototype` property.
3. The constructor function is executed with `this` bound to the new object.
4. If the function does not explicitly return an object, the new object is returned by default.

```js
function Car(make, model) {
  this.make = make;
  this.model = model;
}

const myCar = new Car("Toyota", "Camry");
console.log(myCar); // { make: "Toyota", model: "Camry" }
```

From a syntactic point of view, there’s no special “constructor” keyword (outside of `class`) in JavaScript.
Any function can be used as a constructor simply by calling it with `new`.

Example of misuse:

```js
function Dog(name) {
  this.name = name;
}

const notADog = Dog("Buster"); // this.name is set on global object (or undefined in strict mode)
const properDog = new Dog("Buster"); // creates new Dog instance
```

Modern JavaScript introduces `class` syntax, which clarifies this distinction by enforcing that classes can only be called with `new`.

```js
class Dog {
  constructor(name) {
    this.name = name;
  }
}

const fido = new Dog("Fido");
```

### Return Values in Constructors

Constructors typically don't return anything explicitly.
However, they *can*, depending on what is returned:

* If the constructor returns an object (e.g. `{}`), that object replaces the newly created one.
* If it returns a primitive value (e.g., a string or number), that value is ignored, and the newly constructed object is returned as usual.
* If it returns `undefined`, which is the default, the new object is returned.

```js
function Custom() {
  this.foo = "bar";
  return { override: true };
}

const obj = new Custom();
console.log(obj); // { override: true }
```

In class constructors, this behavior is more restricted.
While base class constructors can return objects, derived classes cannot; doing so will trigger a `TypeError`.

### Prototype Chaining and Inheritance

JavaScript uses a *prototype chain* to implement inheritance.
When a property or method is accessed on an object, JavaScript checks:

1. Does the object itself have the property?
2. If not, it follows the object's internal `[[Prototype]]` link to its constructor’s prototype.
3. This lookup continues up the chain until the property is found or the prototype is `null`.

This mechanism allows methods to be shared and overridden.
If a method exists on a child prototype that matches one higher up the chain, the closer version takes precedence.

```js
function Animal() {}
Animal.prototype.speak = function() {
  return "generic sound";
};

function Dog() {}
Dog.prototype = Object.create(Animal.prototype);
Dog.prototype.constructor = Dog;
Dog.prototype.speak = function() {
  return "woof";
};

const fido = new Dog();
console.log(fido.speak()); // "woof"
```

In this case, `Dog.prototype.speak` overrides `Animal.prototype.speak`.
JavaScript finds the overridden method first when resolving `fido.speak()`.

If desired, the parent method can still be invoked explicitly:

```js
Animal.prototype.speak.call(fido); // "generic sound"
```

This lookup applies to all properties, not just methods:

```js
console.log(Object.getPrototypeOf(fido) === Dog.prototype); // true
console.log(Dog.prototype.__proto__ === Animal.prototype);  // true
```

Prototype chain:

```text
fido → Dog.prototype → Animal.prototype → Object.prototype → null
```

```js
function Animal() {}
Animal.prototype.speak = function() {
  return "generic sound";
};

function Dog() {}
Dog.prototype = Object.create(Animal.prototype);
Dog.prototype.constructor = Dog;

Dog.prototype.speak = function() {
  return "woof";
};

const fido = new Dog();
console.log(fido.speak()); // "woof"
````

In this example, `Dog.prototype.speak` overrides `Animal.prototype.speak`.
When `fido.speak()` is called, JavaScript finds the method on `Dog.prototype` and stops searching.
The `Animal.prototype` version is still present but no longer used unless explicitly called.

An explicit call:

```js
Animal.prototype.speak.call(fido); // "generic sound"
```


### Classes and Modern Syntax

The `class` syntax introduced in ES6 provides a clearer, more familiar way to define constructors and prototypes.
Under the hood, it’s still using the same prototype-based mechanism:

```js
class Animal {
  constructor(name) {
    this.name = name;
  }

  speak() {
    return `${this.name} makes a sound.`;
  }
}

const pet = new Animal("Charlie");
console.log(pet.speak()); // "Charlie makes a sound."
```

Classes provide structure by requiring `new` and limiting constructor behavior.
