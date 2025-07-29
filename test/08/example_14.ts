// Extracted from: docs\Chapters\08.md
// Original example number: 14
// Auto-generated - do not edit directly

const keys = ['A', 'B', 'C'] as const

const MyEnumValues = createEnumFromKeys(keys)
// const MyEnumValues: { A: "A"; B: "B"; C: "C" }

type MyEnum = keyof typeof MyEnumValues
// type MyEnum = "A" | "B" | "C"