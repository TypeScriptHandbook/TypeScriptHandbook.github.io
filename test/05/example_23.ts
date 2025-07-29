// Extracted from: docs\Chapters\05.md
// Original example number: 23
// Auto-generated - do not edit directly

function makeDate(timestamp: number): Date
function makeDate(year: number, month: number, day: number): Date
function makeDate(a: number, b?: number, c?: number): Date {
  if (b !== undefined && c !== undefined) {
    return new Date(a, b - 1, c) // month is 0-indexed
  }
  return new Date(a)
}

const date1 = makeDate(1640995200000) // from timestamp
const date2 = makeDate(2024, 1, 15)   // from year, month, day