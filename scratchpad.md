## Initializing Class Instances

Once you define a class, you can create objects from it using the `new` keyword:

```ts
class User {
  constructor(public name: string, public age: number) {}
}

const u1 = new User("Alice", 30)
```

You can create instances without shorthand by assigning fields inside the constructor body:

```ts
class LegacyUser {
  name: string
  age: number
  constructor(name: string, age: number) {
    this.name = name
    this.age = age
  }
}

const u2 = new LegacyUser("Bob", 45)
```

For classes with optional or default parameters:

```ts
class Config {
  constructor(public env: string = "dev", public debug?: boolean) {}
}

const defaultConfig = new Config()
const prodConfig = new Config("prod", true)
```

You can initialize objects indirectly with factory functions:

```ts
function createPoint(x: number, y: number) {
  return new Point(x, y)
}

const p = createPoint(10, 20)
```

This approach can abstract away class details, allowing you to manage creation logic separately.

### Using Static Factory Methods

Classes can include static methods that return an instance. This is useful when you want multiple ways to construct a class  
or when creation logic involves additional steps.

```ts
class Logger {
  private constructor(public level: string) {}

  static createDebug(): Logger {
    return new Logger("debug")
  }

  static createInfo(): Logger {
    return new Logger("info")
  }
}

const debugLogger = Logger.createDebug()
```

### Dependency Injection

You can inject dependencies during construction, allowing you to pass in collaborators or configuration objects:

```ts
class Service {
  constructor(private fetcher: () => Promise<string>) {}

  async getData() {
    return await this.fetcher()
  }
}

const s = new Service(() => Promise.resolve("fetched data"))
```


