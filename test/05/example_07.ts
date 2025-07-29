// Extracted from: docs\Chapters\05.md
// Original example number: 7
// Auto-generated - do not edit directly

const processUser = (user: User): ProcessedUser => {
  const validated = validateUser(user)
  const normalized = normalizeUser(validated)
  return transformUser(normalized)
}