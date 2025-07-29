// Extracted from: docs\Chapters\09.md
// Original example number: 4
// Auto-generated - do not edit directly

type Cat = { meow: () => void }
type Dog = { bark: () => void }

declare const pet: Cat | Dog

if ("meow" in pet) {
  pet.meow() // narrowed to Cat
} else {
  pet.bark() // narrowed to Dog
}