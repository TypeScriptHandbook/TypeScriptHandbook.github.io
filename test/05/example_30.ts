// Extracted from: docs\Chapters\05.md
// Original example number: 30
// Auto-generated - do not edit directly

interface Database {
  query(sql: string): any[]
}

function executeQuery(this: Database, sql: string): any[] {
  return this.query(sql)
}

const db: Database = {
  query(sql: string) {
    console.log(`Executing: ${sql}`)
    return []
  }
}

// Must call with correct `this` context:
executeQuery.call(db, "SELECT * FROM users") // OK
executeQuery("SELECT * FROM users") // Error: The 'this' context is missing