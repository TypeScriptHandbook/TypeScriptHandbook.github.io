// Extracted from: docs\Chapters\10.md
// Original example number: 9
// Auto-generated - do not edit directly

type Person = {
  name: string
}

type Birthdate = {
  birthdate: Date
}

type PersonWithBirthdate = Person & Birthdate

const individual: PersonWithBirthdate = {
  name: "Alice",
  birthdate: new Date("1990-01-01")
}