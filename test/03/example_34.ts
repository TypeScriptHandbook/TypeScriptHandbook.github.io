// Extracted from: docs\Chapters\03.md
// Original example number: 34
// Language: TypeScript
// Auto-generated - do not edit directly

function processUser(user: { isActive: boolean }): void {
  if (!user.isActive) {
    return // Early exit for inactive users
  }
  // Continue processing active user
  console.log("Updating last seen...")
  console.log("Sending welcome email...")
}