// Extracted from: docs\Chapters\05.md
// Original example number: 36
// Auto-generated - do not edit directly

type EventHandler = () => void

const handler1: EventHandler = () => {
  return "some value" // OK: return value is ignored
}

const handler2: EventHandler = () => {
  console.log("handling event")
  // No return statement - also OK
}

// Both work as event handlers because the return value is ignored
document.addEventListener("click", handler1)
document.addEventListener("click", handler2)