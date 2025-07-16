### Variance

TypeScript has a notion of variance that governs how subtyping works with generic types, particularly when those types are used in function parameters and return values. Understanding variance helps you reason about type relationships and safety in complex type declarations.

#### Variance Annotations

The `in`, `out`, and `in out` keywords express variance explicitly. This feature allows you to document and guide the intended usage of type parameters within your code.

```ts
interface Producer<out T> {
  produce(): T
}

interface Consumer<in T> {
  consume(value: T): void
}

interface Transformer<in out T> {
  transform(value: T): T
}
```

These modifiers mean:

* `out T`: T is used only in output positions (covariant)
* `in T`: T is used only in input positions (contravariant)
* `in out T`: T is used in both directions (invariant)

This syntax allows the compiler and tools to reason more precisely about how types are used, improving expressiveness and safety in generic APIs.

Keep in mind that the actual enforcement of these annotations may still be limited, depending on the compiler settings and ecosystem support, but they represent an important step forward in expressing type relationships directly in TypeScript's type system. for generic type parameters using the `in`, `out`, and `in out` modifiers. These annotations are purely for documentation and tooling—they don’t affect the runtime behavior or type checking yet. They're currently only supported in JSDoc comments, not in `.ts` syntax.

For example, in a `.d.ts` file or JSDoc:

```ts
/**
 * @template out T
 */
type Producer<T> = () => T

/**
 * @template in T
 */
type Consumer<T> = (value: T) => void
```

These annotations indicate intended usage:

* `out T` signals that `T` is used only in output positions (covariant)
* `in T` means `T` is used only in input positions (contravariant)
* `in out T` means the parameter is used in both directions (invariant)

These are helpful when generating documentation or when using tools that interpret variance annotations.

You can still influence variance structurally by how you use types:

```ts
type Covariant<T> = () => T         // T in return position
```

Understanding both structural inference and explicit annotations is useful when authoring libraries or interoperating with documentation-based systems. (like `+T` or `-T` in some other languages). However, you can influence variance through the way types are used:

* Parameters of functions tend to be contravariant
* Return types of functions tend to be covariant
* Properties of objects are invariant if mutable, covariant if readonly

To simulate variance control, TypeScript infers it from usage. For example:

```ts
type Covariant<T> = () => T         // T appears in return position (covariant)
type Contravariant<T> = (x: T) => void // T appears in parameter position (contravariant)
type Invariant<T> = { value: T }    // T appears in both, treated invariant
```

&#x20;Understanding variance helps you reason about type relationships and safety in complex type declarations.

#### Covariance

A type constructor is *covariant* in a type parameter when it preserves the subtyping relationship:

```ts
type ReadOnlyBox<T> = {
  readonly value: T
}

const stringBox: ReadOnlyBox<string> = { value: "hello" }
const widerBox: ReadOnlyBox<string | number> = stringBox // OK
```

Since `ReadOnlyBox` does not allow mutation, it's safe to assign a more specific type to a more general one.

#### Contravariance

Function parameter types are *contravariant*, meaning they reverse the subtyping relationship:

```ts
type Printer<T> = (value: T) => void

const printString: Printer<string> = str => console.log(str)
const printUnknown: Printer<unknown> = printString // OK
```

Here, `printUnknown` can accept any `Printer<T>` for a *specific* `T`, because it's always safe to pass a function that accepts fewer types than the caller expects.

#### Bivariance and Invariance

Function parameters are *bivariant* in some contexts for backwards compatibility, meaning TypeScript may allow both subtype and supertype assignments. This is unsound in strict terms, so enabling `strictFunctionTypes` makes TypeScript enforce proper variance rules.

```ts
type Handler = (event: MouseEvent) => void

const handleUI: Handler = (event: UIEvent) => {
  // Error in strictFunctionTypes: UIEvent not assignable to MouseEvent
}
```

Most types are *invariant* when used in mutable positions:

```ts
type Box<T> = { value: T }

let numberBox: Box<number> = { value: 42 }
// let stringBox: Box<string> = numberBox // Error: Box<string> not assignable to Box<number>
```

Understanding variance allows you to design safer APIs and compose types with confidence.
