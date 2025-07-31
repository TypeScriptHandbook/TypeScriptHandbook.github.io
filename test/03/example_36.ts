// Extracted from: docs\Chapters\03.md
// Original example number: 36
// Language: TypeScript
// Auto-generated - do not edit directly

interface DatabaseConnection {
  connect(): void
}

class DatabaseConnection {
  constructor(private config: any) {}
  connect(): void {
    console.log("Connected to database")
  }
}

// Type-safe configuration with runtime validation
interface DatabaseConfig {
  host: string
  port: number
  ssl: boolean
  credentials?: {
    username: string
    password: string
  }
}

function createConnection(config: DatabaseConfig): DatabaseConnection {
  // Runtime validation
  if (!config.host || config.port <= 0) {
    throw new Error("Invalid database configuration")
  }
  
  // Safe property access with defaults
  const connectionString = `${config.host}:${config.port}`
  const useSSL = config.ssl ?? false
  const auth = config.credentials && {
    user: config.credentials.username,
    pass: config.credentials.password
  }
  
  // Type-safe object construction
  return new DatabaseConnection({
    connectionString,
    ssl: useSSL,
    ...auth && { authentication: auth }
  })
}