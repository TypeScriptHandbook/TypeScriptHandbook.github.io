// Extracted from: docs\Chapters\03.md
// Original example number: 21
// Language: TypeScript
// Auto-generated - do not edit directly

// Add missing helper function
function checkUserPermission(): boolean {
  return Math.random() > 0.5 // Simulate permission check
}

// Boolean logic
const isAuthenticated = true
const hasPermission = checkUserPermission()
const canAccess = isAuthenticated && hasPermission

// Short-circuit evaluation for default values
const user = { name: "", age: 30 }
const username = user.name || "Anonymous"

// Nullish coalescing for more precise defaults
const config = { timeout: 5000 }
const port = config.port ?? 3000 // Only replaces null/undefined, not 0 or ""