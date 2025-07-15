# TypeScript Handbook for Experienced Developers

## Preface

* What This Book Is
* Who It’s For
* How to Read This Book
* What This Book Is Not

---

## Section 1: Context and Philosophy

### Chapter 1.1: JavaScript: The TypeScript Substrate

* A brief (and honest) overview of JavaScript for outsiders
* The good, the bad, and the quirky
* Why TypeScript had to exist

### Chapter 1.2: The Rise of TypeScript

* From superset to superstar
* Influences (e.g. C#, Java, ML)
* Key design goals and tradeoffs

### Chapter 1.3: Structural Typing vs. Nominal Typing

* What structural typing really means
* Advantages and caveats
* Mental models for navigating the system

---

## Section 2: Core Language Tour

### Chapter 2.1: Types, Literals, and Primitives

* Basic types, literal types, template literals
* `any`, `unknown`, `never`, `void`

### Chapter 2.2: Functions and Signatures

* Function types and overloads
* Optional/default/rest parameters
* Function expression vs. declaration

### Chapter 2.3: Objects, Interfaces, and Type Aliases

* Declaring shape types
* Extending and intersecting types
* Index signatures and excess property checks

### Chapter 2.4: Arrays, Tuples, and Readonly Types

* Tuple inference and labels
* `readonly` modifiers and immutability

### Chapter 2.5: Enums and Const Assertions

* Number and string enums
* `as const` for literal inference

---

## Section 3: Advanced Typing and Type Manipulation

### Chapter 3.1: Type Inference and Control

* How inference works
* Type narrowing
* Contextual typing

### Chapter 3.2: Union and Intersection Types

* Discriminated unions
* Exhaustiveness checks
* Common mistakes and clarity techniques

### Chapter 3.3: Generics and Constraints

* Generic functions and types
* Constraint-based design
* Type defaults and inference quirks

### Chapter 3.4: Conditional Types and Mapped Types

* Conditional types, `infer`, and recursion
* Mapped types with modifiers (`+readonly`, `-?`, etc.)

### Chapter 3.5: Template Literal Types and Key Remapping

* Dynamic keys and string pattern types
* `keyof`, `typeof`, and remapping

---

## Section 4: TypeScript in Practice

### Chapter 4.1: Working with JavaScript Libraries

* Typing `import`ed modules
* Declaring types with `declare module`
* Using DefinitelyTyped

### Chapter 4.2: Runtime Validation and Schema Libraries

* Zod, Effect, io-ts, and how they work
* Bridging static types with runtime guarantees

### Chapter 4.3: Branded and Tagged Types

* Preventing accidental mixing (e.g. `UserId` vs. `ProductId`)
* Discriminated unions and runtime tagging

### Chapter 4.4: Type-Level Programming

* Simulating logic in the type system
* Common type-level algorithms (e.g. DeepPartial, Flatten)

---

## Section 5: Interoperability and Ecosystem

### Chapter 5.1: Working with JavaScript

* Type assertions and guards
* The `satisfies` operator
* Dealing with legacy and untyped code

### Chapter 5.2: Configuration and Tooling

* `tsconfig.json` deep dive
* `strict` mode, module resolution, paths
* Project references and monorepos

### Chapter 5.3: Declaration Files and Type Generation

* Writing your own `.d.ts` files
* Using JSDoc to infer types
* Code generation tools

---

## Section 6: Appendix and Reference

### Chapter 6.1: TypeScript Syntax Quick Reference

* A concise syntax-to-feature index

### Chapter 6.2: Common Errors and Diagnostics

* How to read and fix compiler errors
* What `TS2322` *really* means

### Chapter 6.3: Resources for Further Learning

* Books, videos, libraries, tools
* TypeScript evolution (upcoming features)
