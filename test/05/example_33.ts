// Extracted from: docs\Chapters\05.md
// Original example number: 33
// Auto-generated - do not edit directly

function logMessage(message: string): void {
  console.log(message)
  // No explicit return, or return without value
}

function processAsync(data: unknown[]): void {
  data.forEach(item => {
    // Process each item
    console.log(item)
  })
  return // OK: returning nothing from void function
}