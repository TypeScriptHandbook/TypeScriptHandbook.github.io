// Extracted from: docs\Chapters\10.md
// Original example number: 10
// Auto-generated - do not edit directly

type ContactInfo = {
  email: string
  phone: string
}

type Employee = {
  employeeId: number
  department: string
}

type ContactableEmployee = ContactInfo & Employee

const example: ContactableEmployee = {
  email: "jane@example.com",
  phone: "555-1234",
  employeeId: 456,
  department: "Engineering"
}