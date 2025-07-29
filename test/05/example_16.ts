// Extracted from: docs\Chapters\05.md
// Original example number: 16
// Auto-generated - do not edit directly

function logWithLevel(level: string, ...messages: string[]): void {
  console.log(`[${level}]`, ...messages)
}

logWithLevel("INFO", "System", "started", "successfully")
// Output: [INFO] System started successfully