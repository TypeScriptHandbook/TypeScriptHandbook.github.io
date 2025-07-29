// Extracted from: docs\Chapters\02.md
// Original example number: 14
// Auto-generated - do not edit directly

type SystemRole = "admin" | "editor"
type RoleBasedID = `${SystemRole}-${number}`

const editorIdentifier: RoleBasedID = "editor-7"  // OK
// const badIdentifier: RoleBasedID = "user-5"       // Error: "user" is not assignable to type 'SystemRole'