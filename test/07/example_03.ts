// Extracted from: docs\Chapters\07.md
// Original example number: 3
// Auto-generated - do not edit directly

const names: string[] = ["Alice", "Bob", "Carol"]
const scores: number[] = [85, 92, 78]

const upper: string[] = names.map((n: string): string => n.toUpperCase())
console.log(upper) // ["ALICE", "BOB", "CAROL"]

const filtered: string[] = names.filter((n: string): boolean => n.startsWith("A"))
console.log(filtered) // ["Alice"]

const summary: number = scores.reduce((sum: number, score: number): number => sum + score, 0)
console.log(summary) // 255

const report: string = names
  .map((name: string, i: number): string => `${i + 1}. ${name}`)
  .sort()
  .slice(0, 2)
  .join("\n") // join lines into a single string

console.log(report)
// Output:
// 1. Alice
// 2. Bob