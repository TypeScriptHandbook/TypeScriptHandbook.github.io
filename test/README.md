# TypeScript and JavaScript Book Examples Test Directory

Generated on 2025-07-31 15:01:44

This directory contains automatically extracted TypeScript and JavaScript examples from the book chapters.

## Structure
- `package.json` - Dependencies for both TypeScript and JavaScript
- `tsconfig.json` - TypeScript compiler configuration (excludes .js files)
- `chapter*/` - Example directories organized by chapter
- Each chapter contains numbered files with appropriate extensions (.ts or .js)

## Testing Approach
- TypeScript files (.ts) are checked with the TypeScript compiler
- JavaScript files (.js) are checked with Node.js syntax validation
- Examples maintain the order they appear in the markdown files

## Usage
This directory is automatically recreated each time the test script runs.
See `test_results.txt` in the parent directory for consolidated results.
