// Extracted from: docs\Chapters\05.md
// Original example number: 10
// Auto-generated - do not edit directly

function log(message: string, userId?: string): void {
  if (userId) {
    console.log(`[${userId}] ${message}`)
  } else {
    console.log(message)
  }
}

log("System started") // OK
log("User logged in", "user123") // OK