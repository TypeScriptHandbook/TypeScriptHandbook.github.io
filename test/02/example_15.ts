// Extracted from: docs\Chapters\02.md
// Original example number: 15
// Auto-generated - do not edit directly

type ServicePrefix = "api" | "db"
type ResourceName = "user" | "product"
type ServiceEndpoint = `/${ServicePrefix}/${ResourceName}`

const userEndpoint: ServiceEndpoint = "/api/user"     // OK
const productEndpoint: ServiceEndpoint = "/db/product" // OK
// const invalidEndpoint: ServiceEndpoint = "/web/order"    // Error