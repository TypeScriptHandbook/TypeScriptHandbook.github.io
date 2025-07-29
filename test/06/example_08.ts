// Extracted from: docs\Chapters\06.md
// Original example number: 8
// Auto-generated - do not edit directly

class Service {
  constructor(private fetcher: () => Promise<string>) {}

  async getData() {
    return await this.fetcher()
  }
}

const s = new Service(() => Promise.resolve("fetched data"))
s.getData().then(console.log) // "fetched data"