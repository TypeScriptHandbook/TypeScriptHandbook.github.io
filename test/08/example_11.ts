// Extracted from: docs\Chapters\08.md
// Original example number: 11
// Auto-generated - do not edit directly

type Keys = 'Red' | 'Green' | 'Blue'

const ColorEnum: { [K in Keys]: K } = {
  Red: 'Red',
  Green: 'Green',
  Blue: 'Blue'
}