// Extracted from: docs\Chapters\07.md
// Original example number: 2
// Auto-generated - do not edit directly

const fruits = ["apple", "banana", "cherry"]
fruits[0]                      // access by index
fruits.push("date")            // add to the end
const last = fruits.pop()      // remove last item
fruits.unshift("elderberry")   // add to the beginning
const first = fruits.shift()   // remove first item

fruits.forEach((fruit) => console.log(fruit))  // iterate with forEach