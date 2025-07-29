// Extracted from: docs\Chapters\12.md
// Original example number: 9
// Auto-generated - do not edit directly

type ExtractLang<T> = T extends `${infer L}.${string}` ? L : never

type Lang1 = ExtractLang<"en.json"> // "en"
type Lang2 = ExtractLang<"fr.txt">  // "fr"