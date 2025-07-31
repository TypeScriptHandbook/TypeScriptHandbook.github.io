// Extracted from: docs\Chapters\03.md
// Original example number: 22
// Language: TypeScript
// Auto-generated - do not edit directly

interface User {
  profile?: {
    address?: {
      street: string
      city: string
    }
  }
}

function getCity(user: User): string | undefined {
  return user.profile?.address?.city
}

// Works with method calls too
user.processPayment?.()