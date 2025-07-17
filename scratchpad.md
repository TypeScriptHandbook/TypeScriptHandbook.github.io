## Template Literal Types

Template literal types enable constructing new string literal types by concatenating or interpolating string literals:

```ts
// Combine literal types:
type Lang = "en" | "fr"
type FileExtension = ".json" | ".txt"
type Filename = `${Lang}${FileExtension}`

const file: Filename = "en.json" // OK
```

You can use `infer` and `extends` with template literals to extract and manipulate parts of string types:

```ts
type ExtractLang<T> = T extends `${infer L}.${string}` ? L : never

type Lang1 = ExtractLang<"en.json"> // "en"
type Lang2 = ExtractLang<"fr.txt"> // "fr"
```

This allows the type system to analyze string structures at compile time.

## `keyof` and Indexed Access Types

The `keyof` operator produces a union of the keys of a type:

```ts
type Person = {
  name: string
  age: number
}

type PersonKeys = keyof Person // "name" | "age"
```

You can access the type of a specific property using indexed access:

```ts
type AgeType = Person["age"] // number
```

If used with `keyof`, you can define generic utility types:

```ts
type ValueOf<T> = T[keyof T]
type PersonValues = ValueOf<Person> // string | number
```

## `typeof` and `as const`

You can use `typeof` to get the type of a value:

```ts
const config = {
  host: "localhost",
  port: 8080
}

type ConfigType = typeof config
// Equivalent to:
// type ConfigType = { host: string; port: number }
```

When combined with `as const`, you can preserve literal types:

```ts
const status = {
  loading: "loading",
  success: "success"
} as const

// Without `as const`, values would widen to string
// With `as const`, they retain literal values

type Status = typeof status[keyof typeof status] // "loading" | "success"
```

