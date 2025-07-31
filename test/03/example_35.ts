// Extracted from: docs\Chapters\03.md
// Original example number: 35
// Language: TypeScript
// Auto-generated - do not edit directly

async function fetchUserData(id: string): Promise<User> {
  try {
    const response = await fetch(`/api/users/${id}`)
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`)
    }
    return await response.json()
  } catch (error) {
    console.error("Failed to fetch user:", error)
    throw error // Re-throw for caller to handle
  } finally {
    console.log("Fetch attempt completed")
  }
}