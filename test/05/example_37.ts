// Extracted from: docs\Chapters\05.md
// Original example number: 37
// Auto-generated - do not edit directly

// Less specific:
function processData(data: any): any {
  return data.map((item: any) => item.value)
}

// More specific:
function processData<T extends { value: unknown }>(data: T[]): unknown[] {
  return data.map(item => item.value)
}

// Even better with concrete types when possible:
function processUsers(users: User[]): string[] {
  return users.map(user => user.name)
}