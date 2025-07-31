// Extracted from: docs\Chapters\03.md
// Original example number: 9
// Language: TypeScript
// Auto-generated - do not edit directly

const total = calculateTotal(100, 0.08) // Works

function calculateTotal(subtotal: number, taxRate: number): number {
  return subtotal + calculateTax(subtotal, taxRate)
}

function calculateTax(amount: number, rate: number): number {
  return amount * rate
}