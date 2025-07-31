// Extracted from: docs\Chapters\03.md
// Original example number: 15
// Language: TypeScript
// Auto-generated - do not edit directly

type UserAction = 
  | { type: "login"; credentials: string }
  | { type: "logout"; userId: string }
  | { type: "updateProfile"; userId: string; data: any }

function handleUserAction(action: UserAction): void {
  switch (action.type) {
    case "login":
      console.log(`Authenticating with ${action.credentials}`)
      break
    case "logout":
      console.log(`Clearing session for user ${action.userId}`)
      break
    case "updateProfile":
      console.log(`Updating profile for user ${action.userId}`)
      break
    default:
      throw new Error(`Unhandled action: ${action.type}`)
  }
}