// Extracted from: docs\Chapters\03.md
// Original example number: 13
// Language: TypeScript
// Auto-generated - do not edit directly

// user.ts
export interface User {
  id: number
  name: string
}

export function createUser(name: string): User {
  return { id: generateId(), name }
}

// main.ts
import { User, createUser } from "./user"

const newUser: User = createUser("Alice")