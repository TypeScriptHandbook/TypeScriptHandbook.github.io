// Extracted from: docs\Chapters\02.md
// Original example number: 7
// Auto-generated - do not edit directly

type SuccessResult = { status: "ok"; data: string }
type FailureResult = { status: "error"; message: string }
type ApiResult = SuccessResult | FailureResult

function handleApiResult(result: ApiResult) {
  if (result.status === "ok") {
    console.log(result.data) // TypeScript knows this is SuccessResult
  } else {
    console.error(result.message) // TypeScript knows this is FailureResult
  }
}