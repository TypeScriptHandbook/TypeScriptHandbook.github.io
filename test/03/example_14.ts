// Extracted from: docs\Chapters\03.md
// Original example number: 14
// Language: TypeScript
// Auto-generated - do not edit directly

function processOrder(order: { status: string }): void {
  if (order.status === "pending") {
    console.log("Validating order...")
  } else if (order.status === "approved") {
    console.log("Fulfilling order...")
  } else {
    console.log(`Unknown status: ${order.status}`)
  }
}