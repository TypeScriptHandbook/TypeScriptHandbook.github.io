// Extracted from: docs\Chapters\12.md
// Original example number: 21
// Auto-generated - do not edit directly

type EventHandlers<T> = {
  [K in keyof T & string as `on${Capitalize<K>}`]: () => void
}

// Example:
type UI = { click: boolean; focus: boolean }
type Handlers = EventHandlers<UI>
// { onClick: () => void; onFocus: () => void }