// Extracted from: docs\Chapters\06.md
// Original example number: 7
// Auto-generated - do not edit directly

class Logger {
  private constructor(public level: string) {}

  static createDebug(): Logger {
    return new Logger("debug")
  }

  static createInfo(): Logger {
    return new Logger("info")
  }
}

const debugLogger = Logger.createDebug()