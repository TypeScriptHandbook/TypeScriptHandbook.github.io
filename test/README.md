# TypeScript Book Examples Test Directory

This directory contains automatically extracted TypeScript examples from the book chapters.

## Structure

test/
- package.json         # TypeScript dependencies
- tsconfig.json        # TypeScript compiler configuration
- chapter01/           # Examples from Chapter 1
  - example_01.ts
  - example_02.ts
  - ...
- chapter02/           # Examples from Chapter 2
  - example_01.ts
  - ...
- ...

## Usage
Run the test script from the project root:
```bash
python test_examples.py
```

Each chapter directory contains the extracted code examples from that chapter's markdown file.
This directory is automatically recreated each time the test script runs.
