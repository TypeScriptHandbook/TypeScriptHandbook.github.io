// Extracted from: docs\Chapters\01.md
// Original example number: 3
// Auto-generated - do not edit directly

console.log([] + [])  // ""
console.log([] + {})  // "[object Object]"
console.log({} + [])  // 0

console.log(false == 0)   // true
console.log(false === 0)  // false
console.log(NaN === NaN)  // false
console.log(typeof null)  // "object"