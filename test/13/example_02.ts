// Extracted from: docs\Chapters\13.md
// Original example number: 2
// Auto-generated - do not edit directly

// tagged-robot-finder.ts
const log = console.log.bind(console)

type Robot = {
  kind: "robot"
  name: string
  action(): string
}

class RobotClass implements Robot {
  kind: "robot" = "robot"
  constructor(public name: string, private emits: string) {}
  action = (): string => this.emits
}

type Person = {
  kind: "person"
  name: string
  action(): string
}

type Spoof = {
  extra: string
  action(): string
  name: string
  kind: "robot"
}

// Factory function:
function makeSpoof(name: string, act: string): Spoof {
  return {
    action: () => act + " spoof",
    name,
    kind: "robot",
    extra: "foo"
  }
}

// Extend a type with a second type tag:
type RobotWithBigness = Robot & {
  bigness: "very"
}

// Implement extended type:
class BigRobot implements RobotWithBigness {
  kind: "robot" = "robot"
  bigness: "very" = "very"
  constructor(public name: string, private emits: string) {}
  action = (): string => this.emits
}

// Class inheritance:
class LittleRobot extends RobotClass {}

const badRobots: Array<Robot> = [
  // All produce type errors:
  // { kind: "robot", action: () => "informs" }
  // { kind: "robot", name: "K2SO", action: (x: string) => `${x}` },
  // { kind: "robot", name: 11, action: () => 42 },
  // { kind: "person", name: "Alice", action: () => "talks" },
  // { name: "Morty", action: () => "aw geez" },
  // Casts succeed, bad Robots:
  {} as Robot,
  { kind: "robot", name: "Demolition" } as Robot,
  { kind: "robot", action: () => "cleans" } as Robot,
  // 
]

function* robotGenerator(): Generator<Robot, void, unknown> {
  yield new RobotClass("R2D2", "beeps")
  yield { kind: "robot", name: "C3PO", action: () => "informs" }
  yield makeSpoof("K2SO", "security")
  // No upcasting allowed for non-constructed objects:
  // yield { kind:"robot", name: "BB8", action: () => "rolls", bigness:"very" }
  // Upcasting works with a constructed object:
  yield new BigRobot("BB8", "rolls")
  yield new LittleRobot("InsectBot", "flies")
}

const robots = Array.from(robotGenerator())

// Only a constructed class object is findable by instanceof:
robots.forEach(r => {
  // Both checks required, no upcasting for type inheritance,
  // but class inheritance is covered:
  if (r instanceof RobotClass || r instanceof BigRobot)
    log("instanceof:", r.name, r.action())
})

function show(obj: Record<string, unknown>): string {
  return Object
    .entries(obj)
    .sort(([k1], [k2]) => k2.localeCompare(k1))  // reverse sort keys
    .map(([key, value]) => `${key}: ${value}`)
    .join(", ");
}

// Type guard based only on tag:
function isTaggedRobot(x: any): x is Robot {
  return x?.kind === "robot"
}

// Find Robot objects using trusted discriminant:
robots.forEach(r => {
  log(`TaggedRobot [${isTaggedRobot(r)}]: ${show(r)}`)
})
    

// Pattern match on discriminant:
function detect(x: Person | Robot) {
  switch (x.kind) {
    case "person":
      log(x, `detected Person ${x.name}`)
      break
    case "robot":
      log(x, `detected Robot ${x.name}`)
      break
    default:
      log(x, "did not detect Person or Robot")
  }
}

robots.forEach(detect)

// Thorough type guard:
function isExactRobot(value: unknown): value is Robot {
  if (value instanceof RobotClass) return true
  if (typeof value !== "object" || value === null) return false
  const obj = value as Record<string, unknown>
  if (
    obj.kind !== "robot" ||
    typeof obj.name !== "string" ||
    typeof obj.action !== "function"
  ) return false
  // No extra own properties:
  const ownKeys = Object.keys(obj)
  const allowedKeys = ["kind", "name", "action"]
  return (
    ownKeys.length === allowedKeys.length &&
    allowedKeys.every(key => ownKeys.includes(key))
  )
}

robots
  .filter(isExactRobot)
  .forEach(r => log("ExactRobot:", r.name, r.action()))