## Built-in Global Functions

These are part of the global scope and do not require an import statement.
Their behavior may vary slightly between JavaScript environments (e.g., browsers vs. Node.js).

`parseInt`, `parseFloat`: Convert strings to numbers.

```ts
parseInt("42") // 42
parseFloat("3.14") // 3.14
```

`isNaN`, `isFinite`: Test number values.

```ts
isNaN(NaN) // true
isFinite(100) // true
```

`eval`: Executes a string of JavaScript code.

```ts
eval("2 + 2") // 4
```

`encodeURI`, `decodeURI`: Encode/decode a full URI.

```ts
encodeURI("https://example.com/?q=test value")
```

`encodeURIComponent`, `decodeURIComponent`: Encode/decode URI components.

```ts
encodeURIComponent("test value") // "test%20value"
```

`setTimeout`, `setInterval`, `clearTimeout`, `clearInterval`: Timer functions.

```ts
const id = setTimeout(() => console.log("Hello"), 1000)
clearTimeout(id)
```

`alert`, `confirm`, `prompt`: Browser-specific user dialogs.

```ts
alert("Hello")
```

`console.log`, `console.error`, etc.: Logging functions.

```ts
console.log("Debug info")
console.error("Something went wrong")
```
