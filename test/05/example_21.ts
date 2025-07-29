// Extracted from: docs\Chapters\05.md
// Original example number: 21
// Auto-generated - do not edit directly

type Formatter = (template: string, ...args: unknown[]) => string

const formatter: Formatter = (template, ...args) => {
  return template.replace(/{(\d+)}/g, (match, index) => {
    return String(args[parseInt(index)] ?? match)
  })
}

formatter("Hello {0}, you have {1} messages", "Alice", 5)
// "Hello Alice, you have 5 messages"