// Extracted from: docs\Chapters\09.md
// Original example number: 7
// Auto-generated - do not edit directly

type Fish = { swim: () => void }
type Bird = { fly: () => void }

function isFish(pet: Fish | Bird): pet is Fish {
  return (pet as Fish).swim !== undefined
}

declare const pet: Fish | Bird

if (isFish(pet)) {
  pet.swim()
} else {
  pet.fly()
}