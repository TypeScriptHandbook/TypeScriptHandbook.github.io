// Extracted from: docs\Chapters\06.md
// Original example number: 4
// Auto-generated - do not edit directly

class Config {
  constructor(public env: string = "dev", public debug?: boolean) {}
}

const defaultConfig = new Config()
const prodConfig = new Config("prod", true)