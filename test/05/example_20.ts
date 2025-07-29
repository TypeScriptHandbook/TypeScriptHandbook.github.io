// Extracted from: docs\Chapters\05.md
// Original example number: 20
// Auto-generated - do not edit directly

type Logger = (message: string, level?: string) => void

const consoleLogger: Logger = (message, level = "INFO") => {
  console.log(`[${level}] ${message}`)
}