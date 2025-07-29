// Extracted from: docs\Chapters\03.md
// Original example number: 18
// Auto-generated - do not edit directly

const numbers = [1, 2, 3, 4, 5]

// Traditional for loop
for (let i = 0; i < numbers.length; i++) {
  console.log(numbers[i])
}

// for...of iterates over values
for (const number of numbers) {
  console.log(number)
}

// for...in iterates over keys (avoid with arrays)
const user = { name: "Alice", age: 30 }
for (const key in user) {
  console.log(`${key}: ${user[key as keyof typeof user]}`)
}

// while and do-while loops
let count = 0
while (count < 5) {
  console.log(count)
  count++
}