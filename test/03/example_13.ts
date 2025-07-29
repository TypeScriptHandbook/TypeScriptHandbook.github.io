// Extracted from: docs\Chapters\03.md
// Original example number: 13
// Auto-generated - do not edit directly

type Status = "pending" | "approved" | "rejected"
type UserWithStatus = User & { status: Status }

type EventHandler<T> = (event: T) => void