// Extracted from: docs\Chapters\03.md
// Original example number: 26
// Language: TypeScript
// Auto-generated - do not edit directly

type ConfigKeys = keyof Config // "apiUrl" | "timeout" | "retries"

function getConfigValue<K extends keyof Config>(key: K): Config[K] {
  return config[key]
}

const url = getConfigValue("apiUrl") // TypeScript knows this is string