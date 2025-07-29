// Extracted from: docs\Chapters\03.md
// Original example number: 14
// Auto-generated - do not edit directly

enum OrderStatus {
  Pending,
  Processing,
  Shipped,
  Delivered
}

function updateOrder(orderId: string, status: OrderStatus): void {
  console.log(`Order ${orderId} is now ${OrderStatus[status]}`)
}