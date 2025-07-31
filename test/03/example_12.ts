// Extracted from: docs\Chapters\03.md
// Original example number: 12
// Language: TypeScript
// Auto-generated - do not edit directly

interface User {
  id: number
  name: string
  email: string
}

function createUser(userData: User): User {
  return { ...userData, id: Math.floor(Math.random() * 10000) }
}