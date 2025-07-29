// Extracted from: docs\Chapters\06.md
// Original example number: 19
// Auto-generated - do not edit directly

interface User {
  id: number
  name?: string
}

function greet(user: User) {
  if (user.name) {
    console.log(`Hello, ${user.name}`)
  } else {
    console.log("Hello, anonymous user")
  }
}