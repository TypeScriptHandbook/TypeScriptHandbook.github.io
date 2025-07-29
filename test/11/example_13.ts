// Extracted from: docs\Chapters\11.md
// Original example number: 13
// Auto-generated - do not edit directly

interface Producer<out T> {
  produce(): T
}

interface Consumer<in T> {
  consume(value: T): void
}

interface Transformer<in out T> {
  transform(value: T): T
}