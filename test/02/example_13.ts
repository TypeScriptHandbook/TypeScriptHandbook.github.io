// Extracted from: docs\Chapters\02.md
// Original example number: 13
// Auto-generated - do not edit directly

type ProductID = `product-${number}`

function fetchProduct(id: ProductID) {
  return `Fetching product with ID: ${id}`
}

console.log(fetchProduct("product-42"))  // OK
// fetchProduct("item-42") // Error: Argument of type '"item-42"' is not assignable to parameter of type 'ProductID'