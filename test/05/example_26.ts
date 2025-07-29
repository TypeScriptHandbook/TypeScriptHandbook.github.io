// Extracted from: docs\Chapters\05.md
// Original example number: 26
// Auto-generated - do not edit directly

interface User {
  id: number
  name: string
  email: string
}

// Find by ID
function findUser(id: number): Promise<User | null>
// Find by email
function findUser(email: string): Promise<User | null>
// Find by partial match
function findUser(criteria: Partial<User>): Promise<User[]>
// Implementation
function findUser(
  criteria: number | string | Partial<User>
): Promise<User | User[] | null> {
  if (typeof criteria === "number") {
    return findById(criteria)
  }
  if (typeof criteria === "string") {
    return findByEmail(criteria)
  }
  return findByPartial(criteria)
}

// Usage shows clear intent:
const userById = await findUser(123)           // Promise<User | null>
const userByEmail = await findUser("a@b.com")  // Promise<User | null>
const users = await findUser({ name: "Alice" }) // Promise<User[]>